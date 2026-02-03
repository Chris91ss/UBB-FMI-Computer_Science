package com.fitlog.app.ui.diary

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.fitlog.app.databinding.FragmentTodaysDiaryBinding
import com.fitlog.app.vm.MainViewModel
import com.fitlog.app.ui.diary.LoggedFoodAdapter

class TodaysDiaryFragment : Fragment() {

    private var _b: FragmentTodaysDiaryBinding? = null
    private val b get() = _b!!
    private val vm: MainViewModel by activityViewModels()
    private lateinit var adapter: LoggedFoodAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _b = FragmentTodaysDiaryBinding.inflate(inflater, container, false)
        return b.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        adapter = LoggedFoodAdapter(
            onDelete = { loggedFoodId ->
                val action = TodaysDiaryFragmentDirections.actionTodaysDiaryFragmentToConfirmRemoveLoggedFoodDialogFragment(loggedFoodId)
                findNavController().navigate(action)
            }
        )
        b.rvMeals.layoutManager = LinearLayoutManager(requireContext())
        b.rvMeals.adapter = adapter

        b.fabAddMeal.setOnClickListener {
            findNavController().navigate(TodaysDiaryFragmentDirections.actionTodaysDiaryToLogFood())
        }

        vm.loggedFoods.observe(viewLifecycleOwner) { list ->
            adapter.submitList(list)
            val totalKcal = list.sumOf { it.kcalTotal }
            val totalProtein = list.sumOf { it.proteinTotal }
            val totalCarbs = list.sumOf { it.carbsTotal }
            val totalFat = list.sumOf { it.fatTotal }

            // TODO: Replace with actual goals
            val goalKcal = 2000
            val goalProtein = 150
            val goalCarbs = 250
            val goalFat = 60

            b.summaryCalories.text = String.format("%,d", totalKcal)
            b.summaryProtein.text = "%.0fg".format(totalProtein)
            b.summaryCarbs.text = "%.0fg".format(totalCarbs)
            b.summaryFat.text = "%.0fg".format(totalFat)

            b.progressCaloriesSummary.progress = if (goalKcal > 0) (totalKcal * 100 / goalKcal) else 0
            b.progressProteinSummary.progress = if (goalProtein > 0) (totalProtein * 100 / goalProtein).toInt() else 0
            b.progressCarbsSummary.progress = if (goalCarbs > 0) (totalCarbs * 100 / goalCarbs).toInt() else 0
            b.progressFatSummary.progress = if (goalFat > 0) (totalFat * 100 / goalFat).toInt() else 0
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _b = null
    }
}

