import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:logger/logger.dart';
import '../models/sale.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:2626'; // Android emulator localhost
  static final Logger _logger = Logger();

  // GET /sales - Retrieve all sales
  static Future<List<Sale>> getSales() async {
    _logger.i('API: Fetching all sales from $baseUrl/sales');
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/sales'),
      ).timeout(const Duration(seconds: 10));

      _logger.i('API: GET /sales response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final List<dynamic> jsonList = json.decode(response.body);
        final sales = jsonList.map((json) => Sale.fromJson(json)).toList();
        _logger.i('API: Successfully fetched ${sales.length} sales');
        return sales;
      } else {
        _logger.e('API: Failed to fetch sales - Status: ${response.statusCode}');
        throw HttpException('Failed to load sales: ${response.statusCode}');
      }
    } catch (e) {
      _logger.e('API: Error fetching sales: $e');
      rethrow;
    }
  }

  // GET /sale/:id - Retrieve specific sale details
  static Future<Sale> getSaleById(int id) async {
    _logger.i('API: Fetching sale with id: $id');
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/sale/$id'),
      ).timeout(const Duration(seconds: 10));

      _logger.i('API: GET /sale/$id response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final sale = Sale.fromJson(json.decode(response.body));
        _logger.i('API: Successfully fetched sale: $sale');
        return sale;
      } else if (response.statusCode == 404) {
        _logger.e('API: Sale not found with id: $id');
        throw HttpException('Sale not found');
      } else {
        _logger.e('API: Failed to fetch sale - Status: ${response.statusCode}');
        throw HttpException('Failed to load sale: ${response.statusCode}');
      }
    } catch (e) {
      _logger.e('API: Error fetching sale: $e');
      rethrow;
    }
  }

  // POST /sale - Create a new sale
  static Future<Sale> createSale({
    required String date,
    required double amount,
    required String type,
    required String category,
    required String description,
  }) async {
    _logger.i('API: Creating new sale');
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/sale'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'date': date,
          'amount': amount,
          'type': type,
          'category': category,
          'description': description,
        }),
      ).timeout(const Duration(seconds: 10));

      _logger.i('API: POST /sale response status: ${response.statusCode}');

      if (response.statusCode == 201) {
        final sale = Sale.fromJson(json.decode(response.body));
        _logger.i('API: Successfully created sale: $sale');
        return sale;
      } else if (response.statusCode == 400) {
        _logger.e('API: Bad request - Missing required fields');
        throw HttpException('Missing required fields');
      } else {
        _logger.e('API: Failed to create sale - Status: ${response.statusCode}');
        throw HttpException('Failed to create sale: ${response.statusCode}');
      }
    } catch (e) {
      _logger.e('API: Error creating sale: $e');
      rethrow;
    }
  }

  // DELETE /sale/:id - Delete a sale
  static Future<Sale> deleteSale(int id) async {
    _logger.i('API: Deleting sale with id: $id');
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/sale/$id'),
      ).timeout(const Duration(seconds: 10));

      _logger.i('API: DELETE /sale/$id response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final sale = Sale.fromJson(json.decode(response.body));
        _logger.i('API: Successfully deleted sale: $sale');
        return sale;
      } else if (response.statusCode == 404) {
        _logger.e('API: Sale not found with id: $id');
        throw HttpException('Sale not found');
      } else {
        _logger.e('API: Failed to delete sale - Status: ${response.statusCode}');
        throw HttpException('Failed to delete sale: ${response.statusCode}');
      }
    } catch (e) {
      _logger.e('API: Error deleting sale: $e');
      rethrow;
    }
  }

  // GET /allSales - Retrieve all sales for reports/insights
  static Future<List<Sale>> getAllSales() async {
    _logger.i('API: Fetching all sales for reports from $baseUrl/allSales');
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/allSales'),
      ).timeout(const Duration(seconds: 10));

      _logger.i('API: GET /allSales response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final List<dynamic> jsonList = json.decode(response.body);
        final sales = jsonList.map((json) => Sale.fromJson(json)).toList();
        _logger.i('API: Successfully fetched ${sales.length} sales for reports');
        return sales;
      } else {
        _logger.e('API: Failed to fetch all sales - Status: ${response.statusCode}');
        throw HttpException('Failed to load all sales: ${response.statusCode}');
      }
    } catch (e) {
      _logger.e('API: Error fetching all sales: $e');
      rethrow;
    }
  }
}
