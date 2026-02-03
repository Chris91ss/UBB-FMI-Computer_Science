package com.fitlog.app.ui.diary

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.fitlog.app.data.LoggedFood
import com.fitlog.app.databinding.RowAddedMealItemBinding

class LoggedFoodAdapter(
    private val onDelete: (String) -> Unit
) : ListAdapter<LoggedFood, LoggedFoodAdapter.ViewHolder>(DiffCallback) {

    object DiffCallback : DiffUtil.ItemCallback<LoggedFood>() {
        override fun areItemsTheSame(oldItem: LoggedFood, newItem: LoggedFood): Boolean = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: LoggedFood, newItem: LoggedFood): Boolean = oldItem == newItem
    }

    class ViewHolder(private val binding: RowAddedMealItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(loggedFood: LoggedFood, onDelete: (String) -> Unit) {
            binding.name.text = "${loggedFood.food.name} (${loggedFood.grams}g)"
            binding.kcal.text = "${loggedFood.kcalTotal} kcal"
            binding.btnRemove.setOnClickListener { onDelete(loggedFood.id) }

            binding.tvProtein.text = "%.0fg".format(loggedFood.proteinTotal)
            binding.tvCarbs.text = "%.0fg".format(loggedFood.carbsTotal)
            binding.tvFat.text = "%.0fg".format(loggedFood.fatTotal)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = RowAddedMealItemBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position), onDelete)
    }
}

