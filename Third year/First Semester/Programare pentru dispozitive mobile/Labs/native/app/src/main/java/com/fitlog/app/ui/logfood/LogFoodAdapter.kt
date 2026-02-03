package com.fitlog.app.ui.logfood

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.fitlog.app.data.FoodItem
import com.fitlog.app.databinding.RowFoodPickBinding

class LogFoodAdapter(
    private val onAdd: (food: FoodItem, grams: Int) -> Unit,
    private val onEdit: (food: FoodItem) -> Unit,
    private val onDelete: (food: FoodItem) -> Unit
) : ListAdapter<FoodItem, LogFoodAdapter.VH>(Diff) {

    object Diff : DiffUtil.ItemCallback<FoodItem>() {
        override fun areItemsTheSame(o: FoodItem, n: FoodItem) = o.id == n.id
        override fun areContentsTheSame(o: FoodItem, n: FoodItem) = o == n
    }

    inner class VH(val b: RowFoodPickBinding) : RecyclerView.ViewHolder(b.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): VH {
        val inflater = LayoutInflater.from(parent.context)
        val binding = RowFoodPickBinding.inflate(inflater, parent, false)
        return VH(binding)
    }

    override fun onBindViewHolder(h: VH, pos: Int) {
        val food = getItem(pos)
        h.b.name.text = food.name
        h.b.subtitle.text = String.format(
            "Per 100g: %d kcal • %.1fg protein • %.1fg carbs • %.1fg fat",
            food.kcal,
            food.protein,
            food.carbs,
            food.fat
        )

        h.b.btnAdd.setOnClickListener {
            val grams = h.b.grams.text.toString().toIntOrNull() ?: 100
            onAdd(food, grams)
        }
        h.b.btnEdit.setOnClickListener { onEdit(food) }
        h.b.btnDelete.setOnClickListener { onDelete(food) }
    }
}
