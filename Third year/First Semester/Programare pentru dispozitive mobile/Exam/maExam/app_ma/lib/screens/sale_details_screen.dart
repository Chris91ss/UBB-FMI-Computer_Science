import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import '../models/sale.dart';
import '../services/api_service.dart';
import '../services/database_service.dart';

class SaleDetailsScreen extends StatefulWidget {
  final int saleId;

  const SaleDetailsScreen({super.key, required this.saleId});

  @override
  State<SaleDetailsScreen> createState() => _SaleDetailsScreenState();
}

class _SaleDetailsScreenState extends State<SaleDetailsScreen> {
  final Logger _logger = Logger();
  Sale? _sale;
  bool _isLoading = false;
  bool _isOffline = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadSaleDetails();
  }

  Future<void> _loadSaleDetails() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      _logger.i('SaleDetailsScreen: Fetching sale ${widget.saleId} from server');
      final sale = await ApiService.getSaleById(widget.saleId);
      
      // Save to local database for offline access
      await DatabaseService.insertSale(sale);
      _logger.i('SaleDetailsScreen: Sale saved to local database');

      setState(() {
        _sale = sale;
        _isOffline = false;
        _isLoading = false;
      });
    } catch (e) {
      _logger.e('SaleDetailsScreen: Error fetching sale: $e');
      
      // Try to load from local database
      try {
        _logger.i('SaleDetailsScreen: Loading sale from local database');
        final localSale = await DatabaseService.getSaleById(widget.saleId);
        
        if (localSale != null) {
          setState(() {
            _sale = localSale;
            _isOffline = true;
            _isLoading = false;
          });

          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Offline mode: $e'),
                backgroundColor: Colors.orange,
                action: SnackBarAction(
                  label: 'Retry',
                  textColor: Colors.white,
                  onPressed: _loadSaleDetails,
                ),
              ),
            );
          }
        } else {
          setState(() {
            _isLoading = false;
            _isOffline = true;
            _errorMessage = 'Sale not found in local cache';
          });
        }
      } catch (dbError) {
        _logger.e('SaleDetailsScreen: Error loading from local database: $dbError');
        setState(() {
          _isLoading = false;
          _isOffline = true;
          _errorMessage = 'Failed to load sale details. Please try again.';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sale Details'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          if (_isOffline)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Icon(Icons.cloud_off, color: Colors.orange),
            ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isLoading ? null : _loadSaleDetails,
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Loading sale details...'),
          ],
        ),
      );
    }

    if (_errorMessage != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              _errorMessage!,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _loadSaleDetails,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_sale == null) {
      return const Center(
        child: Text('Sale not found'),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          const SizedBox(height: 24),
          _buildDetailCard(),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    final typeColor = _getTypeColor(_sale!.type);
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            CircleAvatar(
              radius: 40,
              backgroundColor: typeColor.withOpacity(0.2),
              child: Icon(
                _getTypeIcon(_sale!.type),
                size: 40,
                color: typeColor,
              ),
            ),
            const SizedBox(height: 16),
            Text(
              '\$${_sale!.amount.toStringAsFixed(2)}',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: typeColor,
              ),
            ),
            const SizedBox(height: 8),
            Chip(
              label: Text(
                _sale!.type.toUpperCase(),
                style: TextStyle(
                  color: typeColor,
                  fontWeight: FontWeight.bold,
                ),
              ),
              backgroundColor: typeColor.withOpacity(0.1),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Details',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const Divider(),
            _buildDetailRow('ID', '#${_sale!.id}'),
            _buildDetailRow('Date', _sale!.date),
            _buildDetailRow('Category', _sale!.category),
            _buildDetailRow('Type', _sale!.type),
            _buildDetailRow(
              'Description',
              _sale!.description.isNotEmpty ? _sale!.description : 'No description',
            ),
            if (_isOffline)
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.orange.shade700, size: 16),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Viewing cached data. Connect to the internet for latest updates.',
                        style: TextStyle(
                          color: Colors.orange.shade700,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: const TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontSize: 16),
            ),
          ),
        ],
      ),
    );
  }

  Color _getTypeColor(String type) {
    switch (type.toLowerCase()) {
      case 'sale':
        return Colors.green;
      case 'lease':
        return Colors.blue;
      case 'rent':
        return Colors.orange;
      default:
        return Colors.grey;
    }
  }

  IconData _getTypeIcon(String type) {
    switch (type.toLowerCase()) {
      case 'sale':
        return Icons.sell;
      case 'lease':
        return Icons.assignment;
      case 'rent':
        return Icons.home;
      default:
        return Icons.business;
    }
  }
}
