import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/food_item.dart';
import '../state/fitlog_model.dart';
import '../widgets/food_form.dart';

class CreateFoodScreen extends StatefulWidget {
  const CreateFoodScreen({super.key});

  @override
  State<CreateFoodScreen> createState() => _CreateFoodScreenState();
}

class _CreateFoodScreenState extends State<CreateFoodScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _servingController = TextEditingController(text: 'per 100 g');
  final _kcalController = TextEditingController();
  final _proteinController = TextEditingController();
  final _carbsController = TextEditingController();
  final _fatController = TextEditingController();
  String? _selectedCategory;

  @override
  void dispose() {
    _nameController.dispose();
    _servingController.dispose();
    _kcalController.dispose();
    _proteinController.dispose();
    _carbsController.dispose();
    _fatController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Create Food')),
        body: FoodForm(
          formKey: _formKey,
          nameController: _nameController,
          servingController: _servingController,
          kcalController: _kcalController,
          proteinController: _proteinController,
          carbsController: _carbsController,
          fatController: _fatController,
          primaryButtonLabel: 'Save Food',
          categories: kFoodCategories,
          selectedCategory: _selectedCategory,
          onCategoryChanged: (value) => setState(() {
            _selectedCategory = value;
          }),
          onSave: _handleSave,
        ),
      );

  Future<void> _handleSave() async {
    if (!_formKey.currentState!.validate()) return;
    final messenger = ScaffoldMessenger.of(context);
    final model = context.read<FitLogModel>();
    final success = await model.createFood(
      FoodItem(
        name: _nameController.text.trim(),
        serving: _servingController.text.trim(),
        kcal: int.parse(_kcalController.text.trim()),
        protein: double.parse(_proteinController.text.trim()),
        carbs: double.parse(_carbsController.text.trim()),
        fat: double.parse(_fatController.text.trim()),
        category: _selectedCategory,
      ),
    );
    if (!mounted) return;
    if (success) {
      Navigator.pop(context);
    } else {
      messenger.showSnackBar(
        const SnackBar(content: Text('Failed to save food. Please try again.')),
      );
    }
  }
}

