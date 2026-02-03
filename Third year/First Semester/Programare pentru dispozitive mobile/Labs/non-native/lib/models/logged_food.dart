import 'food_item.dart';

class LoggedFood {
  const LoggedFood({
    this.id,
    required this.foodId,
    required this.food,
    required this.grams,
  });

  final int? id;
  final int foodId;
  final FoodItem food;
  final int grams;

  int get kcalTotal => (food.kcal / 100 * grams).round();
  double get proteinTotal => food.protein / 100 * grams;
  double get carbsTotal => food.carbs / 100 * grams;
  double get fatTotal => food.fat / 100 * grams;

  LoggedFood copyWith({
    int? id,
    int? foodId,
    FoodItem? food,
    int? grams,
  }) {
    return LoggedFood(
      id: id ?? this.id,
      foodId: foodId ?? this.foodId,
      food: food ?? this.food,
      grams: grams ?? this.grams,
    );
  }
}

