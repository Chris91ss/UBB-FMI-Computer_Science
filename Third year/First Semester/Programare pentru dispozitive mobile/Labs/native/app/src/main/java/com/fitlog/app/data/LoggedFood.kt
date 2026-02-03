package com.fitlog.app.data

data class LoggedFood(
    val id: String, // Unique ID for this specific log entry
    val food: FoodItem,
    var grams: Int
) {
    val kcalTotal get() = (food.kcal / 100.0 * grams).toInt()
    val proteinTotal get() = food.protein / 100.0 * grams
    val carbsTotal get() = food.carbs / 100.0 * grams
    val fatTotal get() = food.fat / 100.0 * grams
}
