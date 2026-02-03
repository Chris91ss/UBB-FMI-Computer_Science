import 'dart:async';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import '../models/sale.dart';
import '../services/api_service.dart';
import '../services/database_service.dart';
import '../services/connectivity_service.dart';
import 'sale_details_screen.dart';
import 'add_sale_screen.dart';

class SalesListScreen extends StatefulWidget {
  const SalesListScreen({super.key});

  @override
  SalesListScreenState createState() => SalesListScreenState();
}

class SalesListScreenState extends State<SalesListScreen> {
  final Logger _logger = Logger();
  List<Sale> _sales = [];
  bool _isLoading = false;
  bool _isOffline = false;
  String? _errorMessage;
  StreamSubscription<bool>? _connectivitySubscription;

  @override
  void initState() {
    super.initState();
    _isOffline = !ConnectivityService.isOnline;
    _loadSales();
    _listenToConnectivity();
  }

  void _listenToConnectivity() {
    _connectivitySubscription = ConnectivityService.onConnectivityChanged.listen((isOnline) {
      _logger.i('SalesListScreen: Connectivity changed - isOnline: $isOnline');
      setState(() => _isOffline = !isOnline);
      
      if (isOnline) {
        // Auto-refresh when coming back online
        _loadSales();
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Back online'),
              backgroundColor: Colors.green,
              duration: Duration(seconds: 2),
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('You are offline'),
              backgroundColor: Colors.orange,
              duration: Duration(seconds: 2),
            ),
          );
        }
      }
    });
  }

  @override
  void dispose() {
    _connectivitySubscription?.cancel();
    super.dispose();
  }

  // Public method to refresh data from parent
  void refresh() {
    _loadSales();
  }

  Future<void> _loadSales() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    // Check connectivity first
    final isOnline = await ConnectivityService.checkConnectivity();
    
    if (!isOnline) {
      // Load from local database when offline
      _logger.i('SalesListScreen: Offline - loading from local database');
      try {
        final localSales = await DatabaseService.getSales();
        setState(() {
          _sales = localSales;
          _isOffline = true;
          _isLoading = false;
        });
      } catch (dbError) {
        _logger.e('SalesListScreen: Error loading from local database: $dbError');
        setState(() {
          _isLoading = false;
          _isOffline = true;
          _errorMessage = 'Failed to load cached data.';
        });
      }
      return;
    }

    try {
      _logger.i('SalesListScreen: Fetching sales from server');
      final sales = await ApiService.getSales();
      
      // Save to local database for offline access
      await DatabaseService.insertSales(sales);
      _logger.i('SalesListScreen: Sales saved to local database');

      setState(() {
        _sales = sales;
        _isOffline = false;
        _isLoading = false;
      });
    } catch (e) {
      _logger.e('SalesListScreen: Error fetching sales: $e');
      
      // Try to load from local database
      try {
        _logger.i('SalesListScreen: Loading sales from local database');
        final localSales = await DatabaseService.getSales();
        
        setState(() {
          _sales = localSales;
          _isOffline = true;
          _isLoading = false;
        });

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Connection error. Showing cached data.'),
              backgroundColor: Colors.orange,
              duration: Duration(seconds: 2),
            ),
          );
        }
      } catch (dbError) {
        _logger.e('SalesListScreen: Error loading from local database: $dbError');
        setState(() {
          _isLoading = false;
          _isOffline = true;
          _errorMessage = 'Failed to load sales. Please try again.';
        });
      }
    }
  }

  Future<void> _deleteSale(Sale sale) async {
    if (_isOffline) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Delete is only available online'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Sale'),
        content: Text('Are you sure you want to delete this ${sale.type} transaction?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirm != true) return;

    setState(() => _isLoading = true);

    try {
      _logger.i('SalesListScreen: Deleting sale ${sale.id}');
      await ApiService.deleteSale(sale.id);
      await DatabaseService.deleteSale(sale.id);
      
      setState(() {
        _sales.removeWhere((s) => s.id == sale.id);
        _isLoading = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Sale deleted successfully'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      _logger.e('SalesListScreen: Error deleting sale: $e');
      setState(() => _isLoading = false);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Failed to delete sale. Check your connection.'),
            backgroundColor: Colors.red,
            duration: Duration(seconds: 2),
          ),
        );
      }
    }
  }

  void _navigateToDetails(Sale sale) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => SaleDetailsScreen(saleId: sale.id),
      ),
    );
  }

  Future<void> _navigateToAddSale() async {
    if (_isOffline) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Add sale is only available online'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    final result = await Navigator.push<bool>(
      context,
      MaterialPageRoute(builder: (context) => const AddSaleScreen()),
    );

    if (result == true) {
      _loadSales();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sales'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          if (_isOffline)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Icon(Icons.cloud_off, color: Colors.orange),
            ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isLoading ? null : _loadSales,
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: _buildBody(),
      floatingActionButton: FloatingActionButton(
        onPressed: _navigateToAddSale,
        tooltip: 'Add Sale',
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading && _sales.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Loading sales...'),
          ],
        ),
      );
    }

    if (_errorMessage != null && _sales.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.cloud_off, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              _errorMessage!,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _loadSales,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_sales.isEmpty) {
      return const Center(
        child: Text('No sales found'),
      );
    }

    return Stack(
      children: [
        RefreshIndicator(
          onRefresh: _loadSales,
          child: ListView.builder(
            itemCount: _sales.length,
            itemBuilder: (context, index) {
              final sale = _sales[index];
              return _buildSaleCard(sale);
            },
          ),
        ),
        if (_isLoading)
          const Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: LinearProgressIndicator(),
          ),
      ],
    );
  }

  Widget _buildSaleCard(Sale sale) {
    final typeColor = _getTypeColor(sale.type);
    
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: typeColor.withOpacity(0.2),
          child: Icon(
            _getTypeIcon(sale.type),
            color: typeColor,
          ),
        ),
        title: Text(
          sale.description.isNotEmpty ? sale.description : '${sale.category} ${sale.type}',
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('${sale.category} • ${sale.date}'),
            Text(
              '\$${sale.amount.toStringAsFixed(2)}',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: typeColor,
              ),
            ),
          ],
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Chip(
              label: Text(
                sale.type,
                style: TextStyle(color: typeColor, fontSize: 12),
              ),
              backgroundColor: typeColor.withOpacity(0.1),
              padding: EdgeInsets.zero,
            ),
            IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () => _deleteSale(sale),
            ),
          ],
        ),
        onTap: () => _navigateToDetails(sale),
        isThreeLine: true,
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
