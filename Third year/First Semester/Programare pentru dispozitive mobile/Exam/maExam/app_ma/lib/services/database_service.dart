import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:logger/logger.dart';
import '../models/sale.dart';

class DatabaseService {
  static Database? _database;
  static final Logger _logger = Logger();

  static Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  static Future<Database> _initDatabase() async {
    _logger.i('DB: Initializing database');
    final path = join(await getDatabasesPath(), 'sales.db');
    _logger.i('DB: Database path: $path');

    return openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        _logger.i('DB: Creating sales table');
        await db.execute('''
          CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT
          )
        ''');
        _logger.i('DB: Sales table created successfully');
      },
    );
  }

  // Insert or update a sale
  static Future<void> insertSale(Sale sale) async {
    _logger.i('DB: Inserting/updating sale: ${sale.id}');
    final db = await database;
    await db.insert(
      'sales',
      sale.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
    _logger.i('DB: Sale ${sale.id} saved successfully');
  }

  // Insert multiple sales (replaces all existing data to sync with server)
  static Future<void> insertSales(List<Sale> sales) async {
    _logger.i('DB: Syncing ${sales.length} sales from server');
    final db = await database;
    
    // Clear existing data and insert fresh server data
    // This ensures local DB matches server state
    await db.delete('sales');
    
    final batch = db.batch();
    for (final sale in sales) {
      batch.insert(
        'sales',
        sale.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
    await batch.commit(noResult: true);
    _logger.i('DB: ${sales.length} sales synced successfully');
  }

  // Get all sales from local database
  static Future<List<Sale>> getSales() async {
    _logger.i('DB: Fetching all sales from local database');
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('sales');
    final sales = maps.map((map) => Sale.fromMap(map)).toList();
    _logger.i('DB: Retrieved ${sales.length} sales from local database');
    return sales;
  }

  // Get a specific sale by ID
  static Future<Sale?> getSaleById(int id) async {
    _logger.i('DB: Fetching sale with id: $id from local database');
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'sales',
      where: 'id = ?',
      whereArgs: [id],
    );
    if (maps.isNotEmpty) {
      final sale = Sale.fromMap(maps.first);
      _logger.i('DB: Found sale: $sale');
      return sale;
    }
    _logger.w('DB: Sale with id: $id not found in local database');
    return null;
  }

  // Delete a sale by ID
  static Future<void> deleteSale(int id) async {
    _logger.i('DB: Deleting sale with id: $id from local database');
    final db = await database;
    await db.delete(
      'sales',
      where: 'id = ?',
      whereArgs: [id],
    );
    _logger.i('DB: Sale $id deleted from local database');
  }

  // Clear all sales
  static Future<void> clearSales() async {
    _logger.i('DB: Clearing all sales from local database');
    final db = await database;
    await db.delete('sales');
    _logger.i('DB: All sales cleared from local database');
  }
}
