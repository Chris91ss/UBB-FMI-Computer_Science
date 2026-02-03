import 'package:flutter/material.dart';

const List<String> kFoodCategories = [
  'Fruits',
  'Vegetables',
  'Meats',
  'Grains',
  'Dairy',
  'Other',
];

class FoodForm extends StatelessWidget {
  const FoodForm({
    super.key,
    required this.formKey,
    required this.nameController,
    required this.servingController,
    required this.kcalController,
    required this.proteinController,
    required this.carbsController,
    required this.fatController,
    required this.onSave,
    required this.primaryButtonLabel,
    required this.categories,
    required this.selectedCategory,
    required this.onCategoryChanged,
  });

  final GlobalKey<FormState> formKey;
  final TextEditingController nameController;
  final TextEditingController servingController;
  final TextEditingController kcalController;
  final TextEditingController proteinController;
  final TextEditingController carbsController;
  final TextEditingController fatController;
  final Future<void> Function() onSave;
  final String primaryButtonLabel;
  final List<String> categories;
  final String? selectedCategory;
  final ValueChanged<String?> onCategoryChanged;

  @override
  Widget build(BuildContext context) {
    return Form(
      key: formKey,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextFormField(
            controller: nameController,
            decoration: const InputDecoration(labelText: 'Food name'),
            textCapitalization: TextCapitalization.words,
            validator: _required,
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: servingController,
            decoration: const InputDecoration(labelText: 'Serving size'),
            validator: _required,
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            value: selectedCategory,
            decoration:
                const InputDecoration(labelText: 'Category (Optional)'),
            hint: const Text('Select category'),
            items: categories
                .map(
                  (category) => DropdownMenuItem(
                    value: category,
                    child: Text(category),
                  ),
                )
                .toList(),
            onChanged: onCategoryChanged,
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: kcalController,
            decoration: const InputDecoration(labelText: 'Calories (kcal)'),
            keyboardType: TextInputType.number,
            validator: _numberRequired,
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  controller: proteinController,
                  decoration: const InputDecoration(labelText: 'Protein (g)'),
                  keyboardType:
                      const TextInputType.numberWithOptions(decimal: true),
                  validator: _numberRequired,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: TextFormField(
                  controller: carbsController,
                  decoration: const InputDecoration(labelText: 'Carbs (g)'),
                  keyboardType:
                      const TextInputType.numberWithOptions(decimal: true),
                  validator: _numberRequired,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: TextFormField(
                  controller: fatController,
                  decoration: const InputDecoration(labelText: 'Fat (g)'),
                  keyboardType:
                      const TextInputType.numberWithOptions(decimal: true),
                  validator: _numberRequired,
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: () {
              onSave();
            },
            child: Text(primaryButtonLabel),
          ),
        ],
      ),
    );
  }

  static String? _required(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Required';
    }
    return null;
  }

  static String? _numberRequired(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Required';
    }
    if (double.tryParse(value) == null) {
      return 'Enter a number';
    }
    return null;
  }
}

