import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';

import '../models/food_item.dart';
import '../models/logged_food.dart';
import 'fitlog_repository.dart';

class FitLogServerRepository {
  FitLogServerRepository({
    required FitLogRepository localRepository,
    String? serverUrl,
  })  : _localRepository = localRepository,
        _serverUrl = serverUrl ?? 'http://localhost:3000',
        _wsUrl = (serverUrl ?? 'http://localhost:3000')
            .replaceFirst('http://', 'ws://')
            .replaceFirst('https://', 'wss://');

  final FitLogRepository _localRepository;
  final String _serverUrl;
  final String _wsUrl;
  
  // Expose local repository for WebSocket updates
  FitLogRepository get localRepository => _localRepository;

  WebSocketChannel? _wsChannel;
  StreamSubscription? _wsSubscription;
  Timer? _connectionCheckTimer;
  bool _isOnline = false;

  // Callback for WebSocket updates
  void Function(String type, dynamic data)? onServerUpdate;
  
  // Callback for connection status changes
  void Function(bool isOnline)? onConnectionStatusChanged;
  
  bool get isOnline => _isOnline;

  // Check if server is reachable
  Future<bool> _checkServerConnection() async {
    try {
      final response = await http
          .get(Uri.parse('$_serverUrl/api/foods'))
          .timeout(const Duration(seconds: 3));
      final wasOnline = _isOnline;
      _isOnline = response.statusCode == 200;
      debugPrint('[ServerRepository] Server connection: ${_isOnline ? "online" : "offline"}');
      
      if (wasOnline != _isOnline && onConnectionStatusChanged != null) {
        onConnectionStatusChanged!(_isOnline);
      }
      
      return _isOnline;
    } catch (e) {
      final wasOnline = _isOnline;
      _isOnline = false;
      debugPrint('[ServerRepository] Server offline: $e');
      
      if (wasOnline != _isOnline && onConnectionStatusChanged != null) {
        onConnectionStatusChanged!(_isOnline);
      }
      
      return false;
    }
  }

  // Connect to WebSocket for real-time updates
  Future<void> connectWebSocket() async {
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Skipping WebSocket connection (server offline)');
      _startPeriodicConnectionCheck();
      return;
    }

    try {
      _wsChannel = WebSocketChannel.connect(Uri.parse(_wsUrl));
      debugPrint('[ServerRepository] WebSocket connected to $_wsUrl');

      _wsSubscription = _wsChannel!.stream.listen(
        (message) {
          try {
            final data = jsonDecode(message);
            final type = data['type'] as String;
            final payload = data['data'];
            debugPrint('[ServerRepository] WebSocket message: $type');
            
            if (onServerUpdate != null) {
              onServerUpdate!(type, payload);
            }
          } catch (e) {
            debugPrint('[ServerRepository] Error parsing WebSocket message: $e');
          }
        },
        onError: (error) {
          debugPrint('[ServerRepository] WebSocket error: $error');
          final wasOnline = _isOnline;
          _isOnline = false;
          if (wasOnline != _isOnline && onConnectionStatusChanged != null) {
            onConnectionStatusChanged!(_isOnline);
          }
          _startPeriodicConnectionCheck();
        },
        onDone: () {
          debugPrint('[ServerRepository] WebSocket closed');
          final wasOnline = _isOnline;
          _isOnline = false;
          if (wasOnline != _isOnline && onConnectionStatusChanged != null) {
            onConnectionStatusChanged!(_isOnline);
          }
          _startPeriodicConnectionCheck();
        },
      );
      
      // Stop periodic check if we're connected
      _connectionCheckTimer?.cancel();
      _connectionCheckTimer = null;
      
      // Process sync queue when coming online
      await _processSyncQueue();
    } catch (e) {
      debugPrint('[ServerRepository] Failed to connect WebSocket: $e');
      _isOnline = false;
      _startPeriodicConnectionCheck();
    }
  }

  // Start periodic connection checking when offline
  void _startPeriodicConnectionCheck() {
    _connectionCheckTimer?.cancel();
    _connectionCheckTimer = Timer.periodic(const Duration(seconds: 5), (timer) async {
      if (!_isOnline) {
        debugPrint('[ServerRepository] Periodic check: Attempting to reconnect...');
        final wasOnline = await _checkServerConnection();
        if (wasOnline) {
          debugPrint('[ServerRepository] Server is back online, connecting WebSocket...');
          await connectWebSocket();
        }
      } else {
        // Already online, stop checking
        timer.cancel();
        _connectionCheckTimer = null;
      }
    });
  }

  // Disconnect WebSocket
  void disconnectWebSocket() {
    _connectionCheckTimer?.cancel();
    _connectionCheckTimer = null;
    _wsSubscription?.cancel();
    _wsChannel?.sink.close();
    _wsChannel = null;
    _wsSubscription = null;
    debugPrint('[ServerRepository] WebSocket disconnected');
  }

  // Fetch foods: get from server, process sync queue
  Future<List<FoodItem>> fetchFoods() async {
    debugPrint('[ServerRepository] Fetching foods...');
    
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, using local DB');
      return _localRepository.fetchFoods();
    }

    try {
      // Process sync queue first
      await _processSyncQueue();
      
      // Then fetch from server
      final response = await http.get(Uri.parse('$_serverUrl/api/foods'));
      
      if (response.statusCode == 200) {
        final List<dynamic> jsonList = jsonDecode(response.body);
        final serverFoods = jsonList.map((json) => FoodItem.fromMap(json)).toList();
        
        // Update local DB with server data (upsert)
        await _localRepository.upsertFoods(serverFoods);
        
        debugPrint('[ServerRepository] Fetched ${serverFoods.length} foods from server');
        return serverFoods;
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, using local DB');
        return _localRepository.fetchFoods();
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, using local DB');
      return _localRepository.fetchFoods();
    }
  }

  // Process sync queue when coming online
  Future<void> _processSyncQueue() async {
    if (!_isOnline) return;
    
    debugPrint('[ServerRepository] Processing sync queue...');
    final pendingOps = await _localRepository.getPendingSyncOperations();
    
    if (pendingOps.isEmpty) {
      debugPrint('[ServerRepository] Sync queue is empty');
      return;
    }
    
    debugPrint('[ServerRepository] Processing ${pendingOps.length} queued operations...');
    
    for (final op in pendingOps) {
      try {
        final operation = op['operation'] as String;
        final entityType = op['entity_type'] as String;
        final entityId = op['entity_id'] as int?;
        final entityData = op['entity_data'] as Map<String, dynamic>;
        final queueId = op['id'] as int;
        
        bool success = false;
        
        if (entityType == 'food') {
          if (operation == 'create') {
            final response = await http.post(
              Uri.parse('$_serverUrl/api/foods'),
              headers: {'Content-Type': 'application/json'},
              body: jsonEncode(entityData),
            );
            if (response.statusCode == 201) {
              final serverFood = FoodItem.fromMap(jsonDecode(response.body));
              // Delete local item with old ID
              if (entityId != null) {
                await _localRepository.deleteFood(entityId);
              }
              // Insert server item with server ID preserved
              await _localRepository.insertFoodWithId(serverFood);
              success = true;
            }
          } else if (operation == 'update' && entityId != null) {
            final response = await http.put(
              Uri.parse('$_serverUrl/api/foods/$entityId'),
              headers: {'Content-Type': 'application/json'},
              body: jsonEncode(entityData),
            );
            if (response.statusCode == 200) {
              final serverFood = FoodItem.fromMap(jsonDecode(response.body));
              // Update local DB with server data
              await _localRepository.updateFood(serverFood);
              success = true;
            }
          } else if (operation == 'delete' && entityId != null) {
            final response = await http.delete(Uri.parse('$_serverUrl/api/foods/$entityId'));
            success = response.statusCode == 204 || response.statusCode == 200;
            // Local DB already deleted when operation was queued
          }
        } else if (entityType == 'logged_food') {
          if (operation == 'create') {
            final response = await http.post(
              Uri.parse('$_serverUrl/api/logged-foods'),
              headers: {'Content-Type': 'application/json'},
              body: jsonEncode(entityData),
            );
            if (response.statusCode == 201) {
              // Delete local item with old ID (it will be re-added from server with correct ID)
              if (entityId != null) {
                await _localRepository.deleteLoggedFood(entityId);
              }
              success = true;
            }
          } else if (operation == 'delete' && entityId != null) {
            final response = await http.delete(Uri.parse('$_serverUrl/api/logged-foods/$entityId'));
            success = response.statusCode == 204 || response.statusCode == 200;
            // Local DB already deleted when operation was queued
          }
        }
        
        if (success) {
          await _localRepository.removeSyncOperation(queueId);
          debugPrint('[ServerRepository] Synced $operation for $entityType (queue ID: $queueId)');
        } else {
          debugPrint('[ServerRepository] Failed to sync $operation for $entityType (queue ID: $queueId)');
        }
      } catch (e) {
        debugPrint('[ServerRepository] Error processing sync operation: $e');
      }
    }
    
    debugPrint('[ServerRepository] Sync queue processing complete');
  }


  // Fetch logged foods: get from server, process sync queue
  Future<List<LoggedFood>> fetchLoggedFoods() async {
    debugPrint('[ServerRepository] Fetching logged foods...');
    
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, using local DB');
      return _localRepository.fetchLoggedFoods();
    }

    try {
      // Process sync queue first (already done in fetchFoods, but ensure it's done)
      await _processSyncQueue();
      
      // Then fetch from server
      final response = await http.get(Uri.parse('$_serverUrl/api/logged-foods'));
      
      if (response.statusCode == 200) {
        final List<dynamic> jsonList = jsonDecode(response.body);
        final serverLogged = jsonList.map((json) {
          return LoggedFood(
            id: json['log_id'] as int,
            foodId: json['id'] as int,
            grams: json['grams'] as int,
            food: FoodItem.fromMap(json),
          );
        }).toList();
        
        // Replace local DB with server data (server is source of truth)
        await _localRepository.replaceLoggedFoodsWithServerData(serverLogged);
        
        debugPrint('[ServerRepository] Fetched ${serverLogged.length} logged foods from server');
        return serverLogged;
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, using local DB');
        return _localRepository.fetchLoggedFoods();
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, using local DB');
      return _localRepository.fetchLoggedFoods();
    }
  }



  // Create food: ALWAYS save to local DB first, then sync to server
  Future<FoodItem> insertFood(FoodItem food) async {
    debugPrint('[ServerRepository] Creating food: ${food.name}');
    
    // ALWAYS save to local DB first (offline-first approach)
    final localSaved = await _localRepository.insertFood(food);
    debugPrint('[ServerRepository] Food saved to local DB with ID: ${localSaved.id}');
    
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, queuing for sync');
      await _localRepository.enqueueSyncOperation(
        operation: 'create',
        entityType: 'food',
        entityId: localSaved.id,
        entityData: food.toMap()..remove('id'),
      );
      return localSaved;
    }

    try {
      // Send to server (server assigns ID)
      final response = await http.post(
        Uri.parse('$_serverUrl/api/foods'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(food.toMap()..remove('id')),
      );

      if (response.statusCode == 201) {
        final json = jsonDecode(response.body);
        final serverSaved = FoodItem.fromMap(json);
        debugPrint('[ServerRepository] Food synced to server with ID: ${serverSaved.id}');
        
        // Update local DB: delete old local ID, insert with server ID
        await _localRepository.deleteFood(localSaved.id!);
        await _localRepository.insertFoodWithId(serverSaved);
        debugPrint('[ServerRepository] Local DB updated with server ID: ${serverSaved.id}');
        return serverSaved;
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, queuing for sync');
        await _localRepository.enqueueSyncOperation(
          operation: 'create',
          entityType: 'food',
          entityId: localSaved.id,
          entityData: food.toMap()..remove('id'),
        );
        return localSaved;
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, queuing for sync');
      await _localRepository.enqueueSyncOperation(
        operation: 'create',
        entityType: 'food',
        entityId: localSaved.id,
        entityData: food.toMap()..remove('id'),
      );
      return localSaved;
    }
  }

  // Update food: send to server, queue if offline
  Future<void> updateFood(FoodItem food) async {
    debugPrint('[ServerRepository] Updating food: ID ${food.id}');
    
    if (food.id == null) {
      throw Exception('Food ID is required for update');
    }

    // Always update local DB first
    await _localRepository.updateFood(food);
    
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, queued for sync');
      // Queue for later sync
      await _localRepository.enqueueSyncOperation(
        operation: 'update',
        entityType: 'food',
        entityId: food.id,
        entityData: food.toMap()..remove('id'),
      );
      return;
    }

    try {
      final response = await http.put(
        Uri.parse('$_serverUrl/api/foods/${food.id}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(food.toMap()..remove('id')),
      );

      if (response.statusCode == 200) {
        debugPrint('[ServerRepository] Food updated on server: ID ${food.id}');
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, queued for sync');
        // Queue for later sync
        await _localRepository.enqueueSyncOperation(
          operation: 'update',
          entityType: 'food',
          entityId: food.id,
          entityData: food.toMap()..remove('id'),
        );
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, queued for sync');
      // Queue for later sync
      await _localRepository.enqueueSyncOperation(
        operation: 'update',
        entityType: 'food',
        entityId: food.id,
        entityData: food.toMap()..remove('id'),
      );
    }
  }

  // Delete food: send to server, queue if offline
  Future<void> deleteFood(int id) async {
    debugPrint('[ServerRepository] Deleting food: ID $id');
    
    // Always delete from local DB first
    await _localRepository.deleteFood(id);
    
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, queued for sync');
      // Queue for later sync
      await _localRepository.enqueueSyncOperation(
        operation: 'delete',
        entityType: 'food',
        entityId: id,
        entityData: {},
      );
      return;
    }

    try {
      final response = await http.delete(Uri.parse('$_serverUrl/api/foods/$id'));

      if (response.statusCode == 204 || response.statusCode == 200) {
        debugPrint('[ServerRepository] Food deleted on server: ID $id');
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, queued for sync');
        // Queue for later sync
        await _localRepository.enqueueSyncOperation(
          operation: 'delete',
          entityType: 'food',
          entityId: id,
          entityData: {},
        );
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, queued for sync');
      // Queue for later sync
      await _localRepository.enqueueSyncOperation(
        operation: 'delete',
        entityType: 'food',
        entityId: id,
        entityData: {},
      );
    }
  }

  // Create logged food: ALWAYS save to local DB first, then sync to server
  Future<LoggedFood> insertLoggedFood({
    required FoodItem food,
    required int grams,
  }) async {
    debugPrint('[ServerRepository] Creating logged food: food_id=${food.id}, grams=$grams');
    
    if (food.id == null) {
      throw Exception('Food ID is required');
    }

    // ALWAYS save to local DB first (offline-first approach)
    final localSaved = await _localRepository.insertLoggedFood(food: food, grams: grams);
    debugPrint('[ServerRepository] Logged food saved to local DB with ID: ${localSaved.id}');

    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, queuing for sync');
      await _localRepository.enqueueSyncOperation(
        operation: 'create',
        entityType: 'logged_food',
        entityId: localSaved.id,
        entityData: {
          'food_id': food.id,
          'grams': grams,
        },
      );
      return localSaved;
    }

    try {
      // Send to server
      final response = await http.post(
        Uri.parse('$_serverUrl/api/logged-foods'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'food_id': food.id,
          'grams': grams,
        }),
      );

      if (response.statusCode == 201) {
        final json = jsonDecode(response.body);
        final serverSaved = LoggedFood(
          id: json['log_id'] as int,
          foodId: json['id'] as int,
          grams: json['grams'] as int,
          food: FoodItem.fromMap(json),
        );
        debugPrint('[ServerRepository] Logged food synced to server with ID: ${serverSaved.id}');
        
        // Update local DB: delete old local ID, insert with server ID
        await _localRepository.deleteLoggedFood(localSaved.id!);
        await _localRepository.insertLoggedFoodWithId(serverSaved);
        debugPrint('[ServerRepository] Local DB updated with server ID: ${serverSaved.id}');
        return serverSaved;
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, queuing for sync');
        await _localRepository.enqueueSyncOperation(
          operation: 'create',
          entityType: 'logged_food',
          entityId: localSaved.id,
          entityData: {
            'food_id': food.id,
            'grams': grams,
          },
        );
        return localSaved;
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, queuing for sync');
      await _localRepository.enqueueSyncOperation(
        operation: 'create',
        entityType: 'logged_food',
        entityId: localSaved.id,
        entityData: {
          'food_id': food.id,
          'grams': grams,
        },
      );
      return localSaved;
    }
  }

  // Delete logged food: send to server, queue if offline
  Future<void> deleteLoggedFood(int id) async {
    debugPrint('[ServerRepository] Deleting logged food: ID $id');
    
    // Always delete from local DB first
    await _localRepository.deleteLoggedFood(id);
    
    if (!await _checkServerConnection()) {
      debugPrint('[ServerRepository] Server offline, queued for sync');
      // Queue for later sync
      await _localRepository.enqueueSyncOperation(
        operation: 'delete',
        entityType: 'logged_food',
        entityId: id,
        entityData: {},
      );
      return;
    }

    try {
      final response = await http.delete(Uri.parse('$_serverUrl/api/logged-foods/$id'));

      if (response.statusCode == 204 || response.statusCode == 200) {
        debugPrint('[ServerRepository] Logged food deleted on server: ID $id');
      } else {
        debugPrint('[ServerRepository] Server error ${response.statusCode}, queued for sync');
        // Queue for later sync
        await _localRepository.enqueueSyncOperation(
          operation: 'delete',
          entityType: 'logged_food',
          entityId: id,
          entityData: {},
        );
      }
    } catch (e) {
      debugPrint('[ServerRepository] Network error: $e, queued for sync');
      // Queue for later sync
      await _localRepository.enqueueSyncOperation(
        operation: 'delete',
        entityType: 'logged_food',
        entityId: id,
        entityData: {},
      );
    }
  }

  // Seed foods (local only, for initial setup)
  Future<void> seedFoodsIfEmpty() async {
    return _localRepository.seedFoodsIfEmpty();
  }
}

