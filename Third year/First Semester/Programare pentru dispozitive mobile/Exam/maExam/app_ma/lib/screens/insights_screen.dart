import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import '../models/sale.dart';
import '../services/api_service.dart';

class InsightsScreen extends StatefulWidget {
  const InsightsScreen({super.key});

  @override
  InsightsScreenState createState() => InsightsScreenState();
}

class InsightsScreenState extends State<InsightsScreen> {
  final Logger _logger = Logger();
  List<CategoryTotal> _categoryTotals = [];
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadInsights();
  }

  // Public method to refresh data from parent
  void refresh() {
    _loadInsights();
  }

  Future<void> _loadInsights() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      _logger.i('InsightsScreen: Fetching all sales for category analysis');
      final sales = await ApiService.getAllSales();
      
      // Compute category totals (by volume = count)
      final categoryMap = <String, CategoryData>{};
      
      for (final sale in sales) {
        final category = sale.category;
        if (categoryMap.containsKey(category)) {
          categoryMap[category]!.count++;
          categoryMap[category]!.totalAmount += sale.amount;
        } else {
          categoryMap[category] = CategoryData(
            count: 1, 
            totalAmount: sale.amount,
          );
        }
      }
      
      // Convert to list and sort descending by volume (count)
      final totals = categoryMap.entries
          .map((e) => CategoryTotal(
                category: e.key,
                volume: e.value.count,
                totalAmount: e.value.totalAmount,
              ))
          .toList();
      totals.sort((a, b) => b.volume.compareTo(a.volume));
      
      // Take top 3
      final top3 = totals.take(3).toList();
      
      _logger.i('InsightsScreen: Computed top ${top3.length} categories');

      setState(() {
        _categoryTotals = top3;
        _isLoading = false;
      });
    } catch (e) {
      _logger.e('InsightsScreen: Error fetching insights: $e');
      
      setState(() {
        _isLoading = false;
        _errorMessage = 'Failed to load insights: $e';
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Top Property Categories'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isLoading ? null : _loadInsights,
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
            Text('Analyzing categories...'),
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
              onPressed: _loadInsights,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_categoryTotals.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.pie_chart_outline, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('No category data available'),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadInsights,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildHeader(),
            const SizedBox(height: 24),
            ..._categoryTotals.asMap().entries.map((entry) {
              return _buildCategoryCard(entry.value, entry.key + 1);
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Card(
      color: Theme.of(context).colorScheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Icon(Icons.leaderboard, size: 48),
            const SizedBox(height: 8),
            const Text(
              'Top 3 Categories by Volume',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              'Based on number of transactions',
              style: TextStyle(
                color: Colors.grey.shade700,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCategoryCard(CategoryTotal categoryTotal, int rank) {
    final colors = [Colors.amber, Colors.grey.shade400, Colors.brown.shade300];
    final icons = [Icons.emoji_events, Icons.workspace_premium, Icons.military_tech];
    
    final color = rank <= 3 ? colors[rank - 1] : Colors.grey;
    final icon = rank <= 3 ? icons[rank - 1] : Icons.category;

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: rank == 1 ? 8 : 4,
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: rank == 1 
              ? Border.all(color: Colors.amber, width: 2)
              : null,
        ),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: color.withOpacity(0.2),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(icon, color: color, size: 32),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '#$rank',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey.shade600,
                          ),
                        ),
                        Text(
                          categoryTotal.category.toUpperCase(),
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildStat(
                    'Volume',
                    '${categoryTotal.volume}',
                    Icons.numbers,
                  ),
                  _buildStat(
                    'Total Amount',
                    '\$${categoryTotal.totalAmount.toStringAsFixed(2)}',
                    Icons.attach_money,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStat(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: Colors.grey, size: 20),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey.shade600,
          ),
        ),
      ],
    );
  }
}

class CategoryData {
  int count;
  double totalAmount;

  CategoryData({required this.count, required this.totalAmount});
}

class CategoryTotal {
  final String category;
  final int volume;
  final double totalAmount;

  CategoryTotal({
    required this.category,
    required this.volume,
    required this.totalAmount,
  });
}
