
package com.fitlog.app.vm
import androidx.lifecycle.LiveData
import androidx.lifecycle.ViewModel
import com.fitlog.app.data.FoodItem
import com.fitlog.app.data.InMemoryRepository
import com.fitlog.app.data.LoggedFood

class MainViewModel : ViewModel() {
    private val repo = InMemoryRepository()
    val foods: LiveData<List<FoodItem>> = repo.foods
    val loggedFoods: LiveData<List<LoggedFood>> = repo.loggedFoods

    fun addFood(item: FoodItem) = repo.addFood(item)
    fun getFood(id: String) = repo.getFood(id)
    fun updateFood(item: FoodItem) = repo.updateFood(item)
    fun deleteFood(id: String) = repo.deleteFood(id)

    fun addLoggedFood(loggedFood: LoggedFood) = repo.addLoggedFood(loggedFood)
    fun deleteLoggedFood(id: String) = repo.deleteLoggedFood(id)

    fun newId() = InMemoryRepository.newId()
}
