
package com.fitlog.app.data
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import java.util.UUID
class InMemoryRepository {
  private val _foods = MutableLiveData<List<FoodItem>>(seedFoods())
  val foods: LiveData<List<FoodItem>> = _foods

  private val _loggedFoods = MutableLiveData<List<LoggedFood>>(emptyList())
  val loggedFoods: LiveData<List<LoggedFood>> = _loggedFoods


  fun getFood(id: String): FoodItem? = _foods.value?.firstOrNull { it.id == id }
  fun addFood(food: FoodItem) { _foods.value = (_foods.value ?: emptyList()) + food }
  fun updateFood(updated: FoodItem) {
      // Update the master list of foods
      _foods.value = (_foods.value ?: emptyList()).map {
          if (it.id == updated.id) updated else it
      }

      // Find any logged foods containing this food and update them
      _loggedFoods.value = (_loggedFoods.value ?: emptyList()).map { loggedFood ->
          if (loggedFood.food.id == updated.id) {
              loggedFood.copy(food = updated)
          } else {
              loggedFood
          }
      }
  }
  fun deleteFood(id: String) {
      _foods.value = (_foods.value ?: emptyList()).filterNot { it.id == id }
      // Also remove any logged entries of this food
      _loggedFoods.value = (_loggedFoods.value ?: emptyList()).filterNot { it.food.id == id }
  }


  fun addLoggedFood(loggedFood: LoggedFood) {
      _loggedFoods.value = (_loggedFoods.value ?: emptyList()) + loggedFood
  }

  fun deleteLoggedFood(id: String) {
      _loggedFoods.value = (_loggedFoods.value ?: emptyList()).filterNot { it.id == id }
  }

  companion object {
    fun newId(): String = UUID.randomUUID().toString()

    private fun seedFoods() = listOf(
      FoodItem(newId(), "Chicken Breast", "per 100 g", 165, 31.0, 0.0, 3.6),
      FoodItem(newId(), "Brown Rice", "per 100 g", 111, 2.6, 23.0, 0.9),
      FoodItem(newId(), "Broccoli", "per 100 g", 34, 2.8, 7.0, 0.4)
    )
  }
}
