
package com.fitlog.app.data
data class FoodItem(
  val id: String,
  var name: String,
  var servingSize: String,
  var kcal: Int,
  var protein: Double,
  var carbs: Double,
  var fat: Double
)
