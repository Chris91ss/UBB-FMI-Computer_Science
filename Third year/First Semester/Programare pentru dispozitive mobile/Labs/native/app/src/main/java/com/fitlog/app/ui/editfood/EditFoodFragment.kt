package com.fitlog.app.ui.editfood

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.core.widget.doOnTextChanged
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.fitlog.app.data.FoodItem
import com.fitlog.app.databinding.FragmentCreateFoodBinding
import com.fitlog.app.vm.MainViewModel

class EditFoodFragment : Fragment() {
    private var _b: FragmentCreateFoodBinding? = null
    private val b get() = _b!!
    private val vm: MainViewModel by activityViewModels()
    private val args: EditFoodFragmentArgs by navArgs()
    private lateinit var originalFood: FoodItem

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        _b = FragmentCreateFoodBinding.inflate(inflater, container, false)
        return b.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        originalFood = vm.getFood(args.foodId) ?: return

        // Pre-populate fields
        b.inputName.setText(originalFood.name)
        b.inputServing.setText(originalFood.servingSize)
        b.inputKcal.setText(originalFood.kcal.toString())
        b.inputProtein.setText(originalFood.protein.toString())
        b.inputCarbs.setText(originalFood.carbs.toString())
        b.inputFat.setText(originalFood.fat.toString())

        // Category Dropdown
        val categories = arrayOf("Fruits", "Vegetables", "Meats", "Grains", "Dairy", "Other")
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, categories)
        b.inputCategory.setAdapter(adapter)

        // Live Nutrition Preview Listeners
        b.inputKcal.doOnTextChanged { _, _, _, _ -> updatePreview() }
        b.inputProtein.doOnTextChanged { _, _, _, _ -> updatePreview() }
        b.inputCarbs.doOnTextChanged { _, _, _, _ -> updatePreview() }
        b.inputFat.doOnTextChanged { _, _, _, _ -> updatePreview() }

        updatePreview() // Initial preview

        // Button Listeners
        b.btnCancel.setOnClickListener { findNavController().navigateUp() }
        b.btnSaveFood.text = "Save Changes"
        b.btnSaveFood.setOnClickListener {
            val name = b.inputName.text?.toString()?.trim().orEmpty()
            if (name.isEmpty()) {
                b.inputName.error = "Required"
                return@setOnClickListener
            }

            val updatedFood = originalFood.copy(
                name = name,
                servingSize = b.inputServing.text.toString(),
                kcal = b.inputKcal.text.toString().toIntOrNull() ?: 0,
                protein = b.inputProtein.text.toString().toDoubleOrNull() ?: 0.0,
                carbs = b.inputCarbs.text.toString().toDoubleOrNull() ?: 0.0,
                fat = b.inputFat.text.toString().toDoubleOrNull() ?: 0.0
            )
            vm.updateFood(updatedFood)
            findNavController().navigateUp()
        }
    }

    private fun updatePreview() {
        val p = b.inputProtein.text?.toString()?.toDoubleOrNull() ?: 0.0
        val c = b.inputCarbs.text?.toString()?.toDoubleOrNull() ?: 0.0
        val f = b.inputFat.text?.toString()?.toDoubleOrNull() ?: 0.0
        val totalMacros = p + c + f

        if (totalMacros > 0) {
            b.progressProtein.progress = (p * 100 / totalMacros).toInt()
            b.progressCarbs.progress = (c * 100 / totalMacros).toInt()
            b.progressFat.progress = (f * 100 / totalMacros).toInt()
        } else {
            b.progressProtein.progress = 0
            b.progressCarbs.progress = 0
            b.progressFat.progress = 0
        }

        b.tvProtein.text = "%.0fg".format(p)
        b.tvCarbs.text = "%.0fg".format(c)
        b.tvFat.text = "%.0fg".format(f)

        val kcal = b.inputKcal.text?.toString()?.toIntOrNull() ?: 0
        b.tvTotalCalories.text = "$kcal kcal"
    }

    override fun onDestroyView() {
        _b = null
        super.onDestroyView()
    }
}
