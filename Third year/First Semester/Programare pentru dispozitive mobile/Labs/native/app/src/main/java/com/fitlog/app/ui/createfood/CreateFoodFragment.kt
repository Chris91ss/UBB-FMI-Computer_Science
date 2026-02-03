
package com.fitlog.app.ui.createfood
import android.os.Bundle
import android.view.*
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import com.fitlog.app.data.FoodItem
import com.fitlog.app.databinding.FragmentCreateFoodBinding
import com.fitlog.app.vm.MainViewModel
import androidx.navigation.fragment.findNavController
import android.widget.ArrayAdapter
import androidx.core.widget.doOnTextChanged

class CreateFoodFragment : Fragment() {
  private var _b: FragmentCreateFoodBinding? = null
  private val b get() = _b!!
  private val vm: MainViewModel by activityViewModels()
  override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?) =
    FragmentCreateFoodBinding.inflate(inflater, container, false).also { _b = it }.root
  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    // Category Dropdown
    val categories = arrayOf("Fruits", "Vegetables", "Meats", "Grains", "Dairy", "Other")
    val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, categories)
    b.inputCategory.setAdapter(adapter)

    // Live Nutrition Preview
    b.inputKcal.doOnTextChanged { _, _, _, _ -> updatePreview() }
    b.inputProtein.doOnTextChanged { _, _, _, _ -> updatePreview() }
    b.inputCarbs.doOnTextChanged { _, _, _, _ -> updatePreview() }
    b.inputFat.doOnTextChanged { _, _, _, _ -> updatePreview() }


    b.btnCancel.setOnClickListener { findNavController().navigateUp() }
    b.btnSaveFood.setOnClickListener {
      val name = b.inputName.text?.toString()?.trim().orEmpty()
      val kcal = b.inputKcal.text?.toString()?.toIntOrNull() ?: 0
      val p = b.inputProtein.text?.toString()?.toDoubleOrNull() ?: 0.0
      val c = b.inputCarbs.text?.toString()?.toDoubleOrNull() ?: 0.0
      val f = b.inputFat.text?.toString()?.toDoubleOrNull() ?: 0.0
      if (name.isEmpty()) { b.inputName.error = "Required"; return@setOnClickListener }
      vm.addFood(FoodItem(vm.newId(), name, "per 100 g", kcal, p, c, f))
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

  override fun onDestroyView() { _b = null; super.onDestroyView() }
}
