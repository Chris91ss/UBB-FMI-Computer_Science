import 'dart:collection';

import 'package:flutter/material.dart';

import '../models/food_item.dart';
import '../models/logged_food.dart';
import '../repository/fitlog_repository.dart';
import '../repository/fitlog_server_repository.dart';

class FitLogModel extends ChangeNotifier {
  FitLogModel({required FitLogServerRepository repository})
      : _repository = repository {
    _initialize();
  }

  final FitLogServerRepository _repository;
  final List<FoodItem> _foods = [];
  final List<LoggedFood> _loggedFoods = [];

  bool _isLoading = true;
  String? _errorMessage;
  bool _isOnline = false;

  bool get isLoading => _isLoading;
  bool get isOnline => _isOnline;
  UnmodifiableListView<FoodItem> get foods => UnmodifiableListView(_foods);
  UnmodifiableListView<LoggedFood> get loggedFoods =>
      UnmodifiableListView(_loggedFoods);

  Future<void> _initialize() async {
    try {
      await _repository.seedFoodsIfEmpty();
      final fetchedFoods = await _repository.fetchFoods();
      final fetchedLogged = await _repository.fetchLoggedFoods();
      _foods
        ..clear()
        ..addAll(fetchedFoods);
      _loggedFoods
        ..clear()
        ..addAll(fetchedLogged);
      
      // Set up WebSocket listener for server updates
      _repository.onServerUpdate = _handleServerUpdate;
      _repository.onConnectionStatusChanged = _updateConnectionStatus;
      await _repository.connectWebSocket();
      _updateConnectionStatus(_repository.isOnline);
      
      // If still offline, periodic check will start automatically
    } catch (error) {
      debugPrint('[FitLogModel] Initialize error: $error');
      _setError('Unable to load data. Please check your connection and try again.');
      _updateConnectionStatus(false);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _updateConnectionStatus(bool online) {
    if (_isOnline != online) {
      _isOnline = online;
      debugPrint('[FitLogModel] Connection status changed: ${online ? "online" : "offline"}');
      notifyListeners();
    }
  }

  void _handleServerUpdate(String type, dynamic data) {
    debugPrint('[FitLogModel] Server update received: $type');
    
    // WebSocket updates are for real-time sync with other clients
    // Local DB is already updated by the repository when we make changes
    // So we only update the in-memory cache here
    
    switch (type) {
      case 'food_created':
        final food = FoodItem.fromMap(data);
        // Only add if not already in cache (prevents duplicates)
        if (!_foods.any((f) => f.id == food.id)) {
          _foods.insert(0, food);
          notifyListeners();
          debugPrint('[FitLogModel] Added food to cache: ${food.name} (ID: ${food.id})');
        }
        break;
      case 'food_updated':
        final food = FoodItem.fromMap(data);
        final index = _foods.indexWhere((f) => f.id == food.id);
        if (index != -1) {
          _foods[index] = food;
          // Update logged foods that reference this food
          for (var i = 0; i < _loggedFoods.length; i++) {
            if (_loggedFoods[i].foodId == food.id) {
              _loggedFoods[i] = _loggedFoods[i].copyWith(food: food);
            }
          }
          notifyListeners();
          debugPrint('[FitLogModel] Updated food in cache: ${food.name} (ID: ${food.id})');
        }
        break;
      case 'food_deleted':
        final id = data['id'] as int;
        final removed = _foods.where((f) => f.id == id).length;
        _foods.removeWhere((f) => f.id == id);
        _loggedFoods.removeWhere((logged) => logged.foodId == id);
        if (removed > 0) {
          notifyListeners();
          debugPrint('[FitLogModel] Removed food from cache: ID $id');
        }
        break;
      case 'logged_food_created':
        final logged = LoggedFood(
          id: data['log_id'] as int,
          foodId: data['id'] as int,
          grams: data['grams'] as int,
          food: FoodItem.fromMap(data),
        );
        // Only add if not already in cache (prevents duplicates)
        if (!_loggedFoods.any((l) => l.id == logged.id)) {
          _loggedFoods.insert(0, logged);
          notifyListeners();
          debugPrint('[FitLogModel] Added logged food to cache: ID ${logged.id}');
        }
        break;
      case 'logged_food_deleted':
        final id = data['id'] as int;
        final removed = _loggedFoods.where((l) => l.id == id).length;
        _loggedFoods.removeWhere((logged) => logged.id == id);
        if (removed > 0) {
          notifyListeners();
          debugPrint('[FitLogModel] Removed logged food from cache: ID $id');
        }
        break;
    }
  }

  @override
  void dispose() {
    _repository.disconnectWebSocket();
    super.dispose();
  }

  FoodItem? getFoodById(int id) {
    try {
      return _foods.firstWhere((f) => f.id == id);
    } catch (_) {
      return null;
    }
  }

  String? consumeError() {
    final error = _errorMessage;
    _errorMessage = null;
    return error;
  }

  Future<bool> createFood(FoodItem food) async {
    debugPrint('[FitLogModel] Creating food: ${food.name}');
    try {
      final saved = await _repository.insertFood(food);
      // When online, WebSocket will update cache
      // When offline, we need to update cache manually
      if (!_isOnline) {
        _foods.insert(0, saved);
        notifyListeners();
        debugPrint('[FitLogModel] Food added to cache (offline): ${saved.name}');
      }
      return true;
    } catch (e) {
      debugPrint('[FitLogModel] Create food error: $e');
      _setError('Unable to save food. Please try again.');
      return false;
    }
  }

  Future<bool> updateFood(FoodItem updated) async {
    if (updated.id == null) return false;
    debugPrint('[FitLogModel] Updating food: ${updated.name} (ID: ${updated.id})');
    try {
      await _repository.updateFood(updated);
      // When online, WebSocket will update cache
      // When offline, we need to update cache manually
      if (!_isOnline) {
        final index = _foods.indexWhere((f) => f.id == updated.id);
        if (index != -1) {
          _foods[index] = updated;
        }
        for (var i = 0; i < _loggedFoods.length; i++) {
          final logged = _loggedFoods[i];
          if (logged.foodId == updated.id) {
            _loggedFoods[i] = logged.copyWith(food: updated);
          }
        }
        notifyListeners();
        debugPrint('[FitLogModel] Food updated in cache (offline): ${updated.name}');
      }
      return true;
    } catch (e) {
      debugPrint('[FitLogModel] Update food error: $e');
      _setError('Unable to update food. Please try again.');
      return false;
    }
  }

  Future<bool> deleteFood(int id) async {
    debugPrint('[FitLogModel] Deleting food: ID $id');
    try {
      await _repository.deleteFood(id);
      // When online, WebSocket will update cache
      // When offline, we need to update cache manually
      if (!_isOnline) {
        _foods.removeWhere((f) => f.id == id);
        _loggedFoods.removeWhere((logged) => logged.foodId == id);
        notifyListeners();
        debugPrint('[FitLogModel] Food removed from cache (offline): ID $id');
      }
      return true;
    } catch (e) {
      debugPrint('[FitLogModel] Delete food error: $e');
      _setError('Unable to delete food. Please try again.');
      return false;
    }
  }

  Future<bool> addLoggedFood({
    required FoodItem food,
    required int grams,
  }) async {
    if (food.id == null) return false;
    debugPrint('[FitLogModel] Adding logged food: ${food.name}, ${grams}g');
    try {
      final saved =
          await _repository.insertLoggedFood(food: food, grams: grams);
      // When online, WebSocket will update cache
      // When offline, we need to update cache manually
      if (!_isOnline) {
        _loggedFoods.insert(0, saved);
        notifyListeners();
        debugPrint('[FitLogModel] Logged food added to cache (offline): ${food.name}');
      }
      return true;
    } catch (e) {
      debugPrint('[FitLogModel] Add logged food error: $e');
      _setError('Unable to add meal. Please try again.');
      return false;
    }
  }

  Future<bool> deleteLoggedFood(int id) async {
    debugPrint('[FitLogModel] Deleting logged food: ID $id');
    try {
      await _repository.deleteLoggedFood(id);
      // When online, WebSocket will update cache
      // When offline, we need to update cache manually
      if (!_isOnline) {
        _loggedFoods.removeWhere((logged) => logged.id == id);
        notifyListeners();
        debugPrint('[FitLogModel] Logged food removed from cache (offline): ID $id');
      }
      return true;
    } catch (e) {
      debugPrint('[FitLogModel] Delete logged food error: $e');
      _setError('Unable to remove meal. Please try again.');
      return false;
    }
  }

  void _setError(String message) {
    debugPrint('[FitLogModel] Error: $message');
    _errorMessage = message;
    notifyListeners();
  }
}

