class FoodItem {
  const FoodItem({
    this.id,
    required this.name,
    required this.serving,
    required this.kcal,
    required this.protein,
    required this.carbs,
    required this.fat,
    this.category,
  });

  final int? id;
  final String name;
  final String serving;
  final int kcal;
  final double protein;
  final double carbs;
  final double fat;
  final String? category;

  FoodItem copyWith({
    int? id,
    String? name,
    String? serving,
    int? kcal,
    double? protein,
    double? carbs,
    double? fat,
    String? category,
  }) {
    return FoodItem(
      id: id ?? this.id,
      name: name ?? this.name,
      serving: serving ?? this.serving,
      kcal: kcal ?? this.kcal,
      protein: protein ?? this.protein,
      carbs: carbs ?? this.carbs,
      fat: fat ?? this.fat,
      category: category ?? this.category,
    );
  }

  Map<String, Object?> toMap() => {
        'id': id,
        'name': name,
        'serving': serving,
        'kcal': kcal,
        'protein': protein,
        'carbs': carbs,
        'fat': fat,
        'category': category,
      };

  factory FoodItem.fromMap(Map<String, Object?> map) => FoodItem(
        id: map['id'] as int?,
        name: map['name'] as String,
        serving: map['serving'] as String,
        kcal: (map['kcal'] as num).toInt(),
        protein: (map['protein'] as num).toDouble(),
        carbs: (map['carbs'] as num).toDouble(),
        fat: (map['fat'] as num).toDouble(),
        category: map['category'] as String?,
      );
}

