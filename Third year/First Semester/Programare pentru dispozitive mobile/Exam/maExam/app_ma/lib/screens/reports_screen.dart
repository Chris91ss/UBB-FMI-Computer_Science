import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import '../models/sale.dart';
import '../services/api_service.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key});

  @override
  ReportsScreenState createState() => ReportsScreenState();
}

class ReportsScreenState extends State<ReportsScreen> {
  final Logger _logger = Logger();
  List<MonthlyTotal> _monthlyTotals = [];
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadReport();
  }

  // Public method to refresh data from parent
  void refresh() {
    _loadReport();
  }

  Future<void> _loadReport() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      _logger.i('ReportsScreen: Fetching all sales for monthly analysis');
      final sales = await ApiService.getAllSales();
      
      // Compute monthly totals
      final monthlyMap = <String, double>{};
      
      for (final sale in sales) {
        // Extract YYYY-MM from date
        final yearMonth = sale.date.substring(0, 7);
        monthlyMap[yearMonth] = (monthlyMap[yearMonth] ?? 0) + sale.amount;
      }
      
      // Convert to list and sort descending by amount
      final totals = monthlyMap.entries
          .map((e) => MonthlyTotal(month: e.key, total: e.value))
          .toList();
      totals.sort((a, b) => b.total.compareTo(a.total));
      
      _logger.i('ReportsScreen: Computed ${totals.length} monthly totals');

      setState(() {
        _monthlyTotals = totals;
        _isLoading = false;
      });
    } catch (e) {
      _logger.e('ReportsScreen: Error fetching report: $e');
      
      setState(() {
        _isLoading = false;
        _errorMessage = 'Failed to load report: $e';
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  String _formatMonth(String yearMonth) {
    final parts = yearMonth.split('-');
    if (parts.length != 2) return yearMonth;
    
    final year = parts[0];
    final month = int.tryParse(parts[1]) ?? 0;
    
    const months = [
      '', 'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    if (month >= 1 && month <= 12) {
      return '${months[month]} $year';
    }
    return yearMonth;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Monthly Sales Analysis'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isLoading ? null : _loadReport,
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
            Text('Computing monthly totals...'),
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
              onPressed: _loadReport,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_monthlyTotals.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.analytics_outlined, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No sales data available'),
          ],
        ),
      );
    }

    // Calculate max for progress bar
    final maxTotal = _monthlyTotals.isNotEmpty
        ? _monthlyTotals.map((e) => e.total).reduce((a, b) => a > b ? a : b)
        : 1.0;

    return RefreshIndicator(
      onRefresh: _loadReport,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _monthlyTotals.length + 1, // +1 for header
        itemBuilder: (context, index) {
          if (index == 0) {
            return _buildHeader();
          }
          final monthlyTotal = _monthlyTotals[index - 1];
          return _buildMonthCard(monthlyTotal, index, maxTotal);
        },
      ),
    );
  }

  Widget _buildHeader() {
    final grandTotal = _monthlyTotals.fold<double>(
      0, (sum, item) => sum + item.total,
    );

    return Card(
      color: Theme.of(context).colorScheme.primaryContainer,
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Icon(Icons.analytics, size: 48),
            const SizedBox(height: 8),
            const Text(
              'Total Sales',
              style: TextStyle(fontSize: 16),
            ),
            Text(
              '\$${grandTotal.toStringAsFixed(2)}',
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              '${_monthlyTotals.length} months',
              style: const TextStyle(color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMonthCard(MonthlyTotal monthlyTotal, int rank, double maxTotal) {
    final progress = monthlyTotal.total / maxTotal;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  radius: 16,
                  backgroundColor: rank <= 3 
                      ? Colors.amber 
                      : Theme.of(context).colorScheme.secondaryContainer,
                  child: Text(
                    '#$rank',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: rank <= 3 ? Colors.white : null,
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    _formatMonth(monthlyTotal.month),
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
                Text(
                  '\$${monthlyTotal.total.toStringAsFixed(2)}',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: progress,
                minHeight: 8,
                backgroundColor: Colors.grey.shade200,
                valueColor: AlwaysStoppedAnimation<Color>(
                  rank <= 3 ? Colors.green : Colors.blue,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class MonthlyTotal {
  final String month;
  final double total;

  MonthlyTotal({required this.month, required this.total});
}
