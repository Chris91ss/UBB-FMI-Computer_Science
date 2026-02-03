import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/food_item.dart';
import '../state/fitlog_model.dart';
import '../widgets/food_form.dart';

class EditFoodScreen extends StatefulWidget {
  const EditFoodScreen({super.key, required this.food});

  final FoodItem food;

  @override
  State<EditFoodScreen> createState() => _EditFoodScreenState();
}

class _EditFoodScreenState extends State<EditFoodScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _nameController;
  late final TextEditingController _servingController;
  late final TextEditingController _kcalController;
  late final TextEditingController _proteinController;
  late final TextEditingController _carbsController;
  late final TextEditingController _fatController;
  String? _selectedCategory;

  @override
  void initState() {
    super.initState();
    final food = widget.food;
    _nameController = TextEditingController(text: food.name);
    _servingController = TextEditingController(text: food.serving);
    _kcalController = TextEditingController(text: food.kcal.toString());
    _proteinController = TextEditingController(text: food.protein.toString());
    _carbsController = TextEditingController(text: food.carbs.toString());
    _fatController = TextEditingController(text: food.fat.toString());
    _selectedCategory = food.category;
  }

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
        appBar: AppBar(title: const Text('Edit Food')),
        body: FoodForm(
          formKey: _formKey,
          nameController: _nameController,
          servingController: _servingController,
          kcalController: _kcalController,
          proteinController: _proteinController,
          carbsController: _carbsController,
          fatController: _fatController,
          primaryButtonLabel: 'Save Changes',
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
    final success = await model.updateFood(
      FoodItem(
        id: widget.food.id,
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
        const SnackBar(content: Text('Failed to update food. Please try again.')),
      );
    }
  }
}

