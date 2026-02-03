import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/logged_food.dart';
import '../state/fitlog_model.dart';
import 'log_food_screen.dart';

class DiaryScreen extends StatelessWidget {
  const DiaryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Today's Diary")),
      body: Consumer<FitLogModel>(
        builder: (context, model, _) {
          final error = model.consumeError();
          if (error != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              if (context.mounted) {
                ScaffoldMessenger.of(context)
                    .showSnackBar(SnackBar(content: Text(error)));
              }
            });
          }

          if (model.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          final loggedFoods = model.loggedFoods;
          final totals = _Totals.from(loggedFoods);
          return Column(
            children: [
              _ConnectionBanner(isOnline: model.isOnline),
              _SummaryCard(totals: totals),
              Expanded(
                child: loggedFoods.isEmpty
                    ? const Center(
                        child: Text('No foods logged yet. Tap + to add one.'),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: loggedFoods.length,
                        itemBuilder: (context, index) =>
                            _LoggedFoodCard(food: loggedFoods[index]),
                      ),
              ),
            ],
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => const LogFoodScreen()),
        ),
        icon: const Icon(Icons.add),
        label: const Text('Add Food'),
      ),
    );
  }
}

class _ConnectionBanner extends StatelessWidget {
  const _ConnectionBanner({required this.isOnline});

  final bool isOnline;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      color: isOnline ? Colors.green.shade100 : Colors.orange.shade100,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            isOnline ? Icons.cloud_done : Icons.cloud_off,
            size: 16,
            color: isOnline ? Colors.green.shade700 : Colors.orange.shade700,
          ),
          const SizedBox(width: 8),
          Text(
            isOnline ? 'Online - Syncing with server' : 'Offline - Using local data',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: isOnline ? Colors.green.shade700 : Colors.orange.shade700,
            ),
          ),
        ],
      ),
    );
  }
}

class _SummaryCard extends StatelessWidget {
  const _SummaryCard({required this.totals});

  final _Totals totals;

  @override
  Widget build(BuildContext context) {
    const goalKcal = 2000;
    const goalProtein = 150.0;
    const goalCarbs = 250.0;
    const goalFat = 60.0;

    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Today\'s Summary',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _SummaryRow(
              label: 'Calories',
              value: '${totals.kcal} kcal',
              goalLabel: '$goalKcal kcal goal',
              progress: totals.kcal / goalKcal,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 12),
            _MacroRow(
              label: 'Protein',
              grams: totals.protein,
              goal: goalProtein,
              color: Colors.green,
            ),
            _MacroRow(
              label: 'Carbs',
              grams: totals.carbs,
              goal: goalCarbs,
              color: Colors.orange,
            ),
            _MacroRow(
              label: 'Fat',
              grams: totals.fat,
              goal: goalFat,
              color: Colors.redAccent,
            ),
          ],
        ),
      ),
    );
  }
}

class _SummaryRow extends StatelessWidget {
  const _SummaryRow({
    required this.label,
    required this.value,
    required this.goalLabel,
    required this.progress,
    required this.color,
  });

  final String label;
  final String value;
  final String goalLabel;
  final double progress;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: Theme.of(context).textTheme.bodyLarge),
            Text(value, style: Theme.of(context).textTheme.titleMedium),
          ],
        ),
        const SizedBox(height: 4),
        LinearProgressIndicator(
          value: progress.clamp(0.0, 1.0),
          color: color,
          backgroundColor: color.withOpacity(.2),
        ),
        const SizedBox(height: 4),
        Text(goalLabel, style: Theme.of(context).textTheme.bodySmall),
      ],
    );
  }
}

class _MacroRow extends StatelessWidget {
  const _MacroRow({
    required this.label,
    required this.grams,
    required this.goal,
    required this.color,
  });

  final String label;
  final double grams;
  final double goal;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: Theme.of(context).textTheme.bodyLarge),
              Text('${grams.toStringAsFixed(0)}g',
                  style: Theme.of(context)
                      .textTheme
                      .titleMedium
                      ?.copyWith(color: color)),
            ],
          ),
          SizedBox(
            width: 160,
            child: LinearProgressIndicator(
              value: (grams / goal).clamp(0.0, 1.0),
              color: color,
              backgroundColor: color.withOpacity(.2),
            ),
          ),
        ],
      ),
    );
  }
}

class _LoggedFoodCard extends StatelessWidget {
  const _LoggedFoodCard({required this.food});

  final LoggedFood food;

  @override
  Widget build(BuildContext context) {
    final model = context.read<FitLogModel>();
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    '${food.food.name} (${food.grams} g)',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
                TextButton(
                  onPressed: () => _confirmRemoval(context, model),
                  child: const Text('Remove'),
                ),
              ],
            ),
            if (food.food.category?.isNotEmpty == true)
              Text(
                food.food.category!,
                style: Theme.of(context).textTheme.bodySmall,
              ),
            Text(
              '${food.kcalTotal} kcal',
              style: Theme.of(context)
                  .textTheme
                  .titleLarge
                  ?.copyWith(color: Theme.of(context).colorScheme.primary),
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _MacroChip(label: 'Protein', value: food.proteinTotal),
                _MacroChip(label: 'Carbs', value: food.carbsTotal),
                _MacroChip(label: 'Fat', value: food.fatTotal),
              ],
            )
          ],
        ),
      ),
    );
  }

  Future<void> _confirmRemoval(BuildContext context, FitLogModel model) async {
    final shouldDelete = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Remove food?'),
        content: const Text(
          'This will remove the food from today\'s diary. This cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Remove'),
          ),
        ],
      ),
    );
    if (shouldDelete == true && food.id != null) {
      final success = await model.deleteLoggedFood(food.id!);
      if (!success && context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to remove meal.')),
        );
      }
    }
  }
}

class _MacroChip extends StatelessWidget {
  const _MacroChip({required this.label, required this.value});

  final String label;
  final double value;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: Theme.of(context).textTheme.bodySmall),
        Text(
          '${value.toStringAsFixed(0)} g',
          style: Theme.of(context).textTheme.titleMedium,
        ),
      ],
    );
  }
}

class _Totals {
  const _Totals({
    required this.kcal,
    required this.protein,
    required this.carbs,
    required this.fat,
  });

  final int kcal;
  final double protein;
  final double carbs;
  final double fat;

  factory _Totals.from(List<LoggedFood> foods) {
    var kcal = 0;
    var protein = 0.0;
    var carbs = 0.0;
    var fat = 0.0;
    for (final food in foods) {
      kcal += food.kcalTotal;
      protein += food.proteinTotal;
      carbs += food.carbsTotal;
      fat += food.fatTotal;
    }
    return _Totals(kcal: kcal, protein: protein, carbs: carbs, fat: fat);
  }
}

