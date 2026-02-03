import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:sqflite/sqflite.dart';

import '../db/fitlog_database.dart';
import '../models/food_item.dart';
import '../models/logged_food.dart';

class FitLogRepository {
  FitLogRepository({FitLogDatabase? database})
      : _databaseProvider = database ?? FitLogDatabase.instance;

  final FitLogDatabase _databaseProvider;

  Future<Database> get _db async => _databaseProvider.database;

  Future<List<FoodItem>> fetchFoods() async {
    try {
      final db = await _db;
      final maps = await db.query('foods', orderBy: 'id DESC');
      return maps.map((map) => FoodItem.fromMap(map)).toList();
    } catch (error, stack) {
      debugPrint('Failed to fetch foods: $error\n$stack');
      rethrow;
    }
  }

  Future<FoodItem?> getFoodById(int id) async {
    try {
      final db = await _db;
      final maps = await db.query('foods', where: 'id = ?', whereArgs: [id], limit: 1);
      if (maps.isEmpty) return null;
      return FoodItem.fromMap(maps.first);
    } catch (error, stack) {
      debugPrint('Failed to get food by ID: $error\n$stack');
      return null;
    }
  }

  Future<List<LoggedFood>> fetchLoggedFoods() async {
    try {
      final db = await _db;
      final rows = await db.rawQuery('''
        SELECT lf.id as log_id, lf.grams, f.*
        FROM logged_foods lf
        INNER JOIN foods f ON f.id = lf.food_id
        ORDER BY lf.id DESC;
      ''');
      return rows
          .map(
            (row) => LoggedFood(
              id: row['log_id'] as int,
              foodId: row['id'] as int,
              grams: row['grams'] as int,
              food: FoodItem.fromMap(row),
            ),
          )
          .toList();
    } catch (error, stack) {
      debugPrint('Failed to fetch logged foods: $error\n$stack');
      rethrow;
    }
  }

  Future<FoodItem> insertFood(FoodItem food) async {
    try {
      final db = await _db;
      final id = await db.insert('foods', food.toMap()..remove('id'));
      return food.copyWith(id: id);
    } catch (error, stack) {
      debugPrint('Failed to insert food: $error\n$stack');
      rethrow;
    }
  }

  // Insert food with specific ID (for syncing server items)
  Future<FoodItem> insertFoodWithId(FoodItem food) async {
    try {
      final db = await _db;
      if (food.id == null) {
        return await insertFood(food);
      }
      // Use INSERT OR REPLACE to handle duplicate IDs
      await db.rawInsert(
        'INSERT OR REPLACE INTO foods (id, name, serving, kcal, protein, carbs, fat, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        [food.id, food.name, food.serving, food.kcal, food.protein, food.carbs, food.fat, food.category],
      );
      debugPrint('[LocalRepository] Inserted food with ID: ${food.id}');
      return food;
    } catch (error, stack) {
      debugPrint('Failed to insert food with ID: $error\n$stack');
      rethrow;
    }
  }

  // Insert logged food with specific ID (for syncing server items)
  Future<LoggedFood> insertLoggedFoodWithId(LoggedFood loggedFood) async {
    try {
      final db = await _db;
      if (loggedFood.id == null) {
        return await insertLoggedFood(food: loggedFood.food, grams: loggedFood.grams);
      }
      // Use INSERT OR REPLACE to handle duplicate IDs
      await db.rawInsert(
        'INSERT OR REPLACE INTO logged_foods (id, food_id, grams) VALUES (?, ?, ?)',
        [loggedFood.id, loggedFood.foodId, loggedFood.grams],
      );
      debugPrint('[LocalRepository] Inserted logged food with ID: ${loggedFood.id}');
      return loggedFood;
    } catch (error, stack) {
      debugPrint('Failed to insert logged food with ID: $error\n$stack');
      rethrow;
    }
  }

  Future<void> updateFood(FoodItem food) async {
    try {
      final db = await _db;
      await db.update(
        'foods',
        food.toMap()..remove('id'),
        where: 'id = ?',
        whereArgs: [food.id],
      );
    } catch (error, stack) {
      debugPrint('Failed to update food: $error\n$stack');
      rethrow;
    }
  }

  Future<void> deleteFood(int id) async {
    try {
      final db = await _db;
      await db.delete('logged_foods', where: 'food_id = ?', whereArgs: [id]);
      await db.delete('foods', where: 'id = ?', whereArgs: [id]);
    } catch (error, stack) {
      debugPrint('Failed to delete food: $error\n$stack');
      rethrow;
    }
  }

  Future<LoggedFood> insertLoggedFood({
    required FoodItem food,
    required int grams,
  }) async {
    try {
      final db = await _db;
      final id = await db.insert('logged_foods', {
        'food_id': food.id,
        'grams': grams,
      });
      return LoggedFood(
        id: id,
        foodId: food.id!,
        food: food,
        grams: grams,
      );
    } catch (error, stack) {
      debugPrint('Failed to insert logged food: $error\n$stack');
      rethrow;
    }
  }

  Future<void> deleteLoggedFood(int id) async {
    try {
      final db = await _db;
      await db.delete('logged_foods', where: 'id = ?', whereArgs: [id]);
    } catch (error, stack) {
      debugPrint('Failed to delete logged food: $error\n$stack');
      rethrow;
    }
  }

  Future<void> seedFoodsIfEmpty() async {
    final db = await _db;
    final count =
        Sqflite.firstIntValue(await db.rawQuery('SELECT COUNT(*) FROM foods')) ??
            0;
    if (count > 0) return;

    final seeds = [
      const FoodItem(
        name: 'Chicken Breast',
        serving: 'per 100 g',
        kcal: 165,
        protein: 31,
        carbs: 0,
        fat: 4,
        category: 'Meats',
      ),
      const FoodItem(
        name: 'Brown Rice',
        serving: 'per 100 g',
        kcal: 111,
        protein: 3,
        carbs: 23,
        fat: 1,
        category: 'Grains',
      ),
      const FoodItem(
        name: 'Broccoli',
        serving: 'per 100 g',
        kcal: 34,
        protein: 3,
        carbs: 7,
        fat: 0,
        category: 'Vegetables',
      ),
    ];

    for (final food in seeds) {
      await insertFood(food);
    }
  }

  // Upsert foods (insert or update, don't delete all)
  Future<void> upsertFoods(List<FoodItem> foods) async {
    try {
      final db = await _db;
      await db.transaction((txn) async {
        for (final food in foods) {
          if (food.id == null) continue;
          final existing = await txn.query(
            'foods',
            where: 'id = ?',
            whereArgs: [food.id],
          );
          if (existing.isEmpty) {
            // Insert new
            await txn.insert('foods', food.toMap());
          } else {
            // Update existing
            await txn.update(
              'foods',
              food.toMap()..remove('id'),
              where: 'id = ?',
              whereArgs: [food.id],
            );
          }
        }
      });
      debugPrint('[LocalRepository] Upserted ${foods.length} foods to local DB');
    } catch (error, stack) {
      debugPrint('Failed to upsert foods: $error\n$stack');
      rethrow;
    }
  }

  // Replace local DB with server data (server is source of truth when online)
  Future<void> replaceFoodsWithServerData(List<FoodItem> serverFoods) async {
    try {
      final db = await _db;
      await db.transaction((txn) async {
        // Get all local food IDs
        final localFoods = await txn.query('foods', columns: ['id']);
        final localIds = localFoods.map((f) => f['id'] as int).toSet();
        final serverIds = serverFoods.where((f) => f.id != null).map((f) => f.id!).toSet();
        
        // Delete local items not on server (orphaned items)
        final toDelete = localIds.difference(serverIds);
        for (final id in toDelete) {
          await txn.delete('foods', where: 'id = ?', whereArgs: [id]);
        }
        
        // Upsert server items
        for (final food in serverFoods) {
          if (food.id == null) continue;
          final existing = await txn.query('foods', where: 'id = ?', whereArgs: [food.id], limit: 1);
          if (existing.isEmpty) {
            await txn.insert('foods', food.toMap());
          } else {
            await txn.update('foods', food.toMap()..remove('id'), where: 'id = ?', whereArgs: [food.id]);
          }
        }
      });
      debugPrint('[LocalRepository] Replaced local foods with ${serverFoods.length} server foods');
    } catch (error, stack) {
      debugPrint('Failed to replace foods with server data: $error\n$stack');
      rethrow;
    }
  }

  // Replace local DB with server data (server is source of truth when online)
  Future<void> replaceLoggedFoodsWithServerData(List<LoggedFood> serverLogged) async {
    try {
      final db = await _db;
      await db.transaction((txn) async {
        // Get all local logged food IDs
        final localLogged = await txn.query('logged_foods', columns: ['id']);
        final localIds = localLogged.map((l) => l['id'] as int).toSet();
        final serverIds = serverLogged.where((l) => l.id != null).map((l) => l.id!).toSet();
        
        // Delete local items not on server (orphaned items)
        final toDelete = localIds.difference(serverIds);
        for (final id in toDelete) {
          await txn.delete('logged_foods', where: 'id = ?', whereArgs: [id]);
        }
        
        // Upsert server items
        for (final logged in serverLogged) {
          if (logged.id == null) continue;
          final existing = await txn.query('logged_foods', where: 'id = ?', whereArgs: [logged.id], limit: 1);
          if (existing.isEmpty) {
            await txn.rawInsert(
              'INSERT OR REPLACE INTO logged_foods (id, food_id, grams) VALUES (?, ?, ?)',
              [logged.id, logged.foodId, logged.grams],
            );
          } else {
            await txn.update('logged_foods', {
              'food_id': logged.foodId,
              'grams': logged.grams,
            }, where: 'id = ?', whereArgs: [logged.id]);
          }
        }
      });
      debugPrint('[LocalRepository] Replaced local logged foods with ${serverLogged.length} server logged foods');
    } catch (error, stack) {
      debugPrint('Failed to replace logged foods with server data: $error\n$stack');
      rethrow;
    }
  }

  // Upsert logged foods (insert or update, don't delete all)
  Future<void> upsertLoggedFoods(List<LoggedFood> loggedFoods) async {
    try {
      final db = await _db;
      await db.transaction((txn) async {
        for (final logged in loggedFoods) {
          final existing = await txn.query(
            'logged_foods',
            where: 'id = ?',
            whereArgs: [logged.id],
          );
          if (existing.isEmpty) {
            // Insert new - use INSERT OR REPLACE to handle ID conflicts
            await txn.rawInsert(
              'INSERT OR REPLACE INTO logged_foods (id, food_id, grams) VALUES (?, ?, ?)',
              [logged.id, logged.foodId, logged.grams],
            );
          } else {
            // Update existing
            await txn.update(
              'logged_foods',
              {
                'food_id': logged.foodId,
                'grams': logged.grams,
              },
              where: 'id = ?',
              whereArgs: [logged.id],
            );
          }
        }
      });
      debugPrint('[LocalRepository] Upserted ${loggedFoods.length} logged foods to local DB');
    } catch (error, stack) {
      debugPrint('Failed to upsert logged foods: $error\n$stack');
      rethrow;
    }
  }

  // Sync queue operations
  Future<void> enqueueSyncOperation({
    required String operation, // 'create', 'update', 'delete'
    required String entityType, // 'food', 'logged_food'
    int? entityId,
    required Map<String, dynamic> entityData,
  }) async {
    try {
      final db = await _db;
      await db.insert('sync_queue', {
        'operation': operation,
        'entity_type': entityType,
        'entity_id': entityId,
        'entity_data': jsonEncode(entityData),
        'created_at': DateTime.now().millisecondsSinceEpoch,
      });
      debugPrint('[LocalRepository] Enqueued $operation for $entityType (ID: $entityId)');
    } catch (error, stack) {
      debugPrint('Failed to enqueue sync operation: $error\n$stack');
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> getPendingSyncOperations() async {
    try {
      final db = await _db;
      final maps = await db.query('sync_queue', orderBy: 'created_at ASC');
      return maps.map((map) => {
        'id': map['id'] as int,
        'operation': map['operation'] as String,
        'entity_type': map['entity_type'] as String,
        'entity_id': map['entity_id'] as int?,
        'entity_data': jsonDecode(map['entity_data'] as String),
        'created_at': map['created_at'] as int,
      }).toList();
    } catch (error, stack) {
      debugPrint('Failed to get pending sync operations: $error\n$stack');
      rethrow;
    }
  }

  Future<void> removeSyncOperation(int queueId) async {
    try {
      final db = await _db;
      await db.delete('sync_queue', where: 'id = ?', whereArgs: [queueId]);
      debugPrint('[LocalRepository] Removed sync operation from queue (ID: $queueId)');
    } catch (error, stack) {
      debugPrint('Failed to remove sync operation: $error\n$stack');
      rethrow;
    }
  }
}

