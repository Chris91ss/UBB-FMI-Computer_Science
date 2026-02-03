package com.fitlog.app.ui.logfood

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.fitlog.app.data.LoggedFood
import com.fitlog.app.databinding.FragmentLogFoodBinding
import com.fitlog.app.vm.MainViewModel

class LogFoodFragment : Fragment() {

    private var _b: FragmentLogFoodBinding? = null
    private val b get() = _b!!
    private val vm: MainViewModel by activityViewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _b = FragmentLogFoodBinding.inflate(inflater, container, false)
        return b.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val adapter = LogFoodAdapter(
            onAdd = { food, grams ->
                val loggedFood = LoggedFood(
                    id = vm.newId(),
                    food = food,
                    grams = grams
                )
                vm.addLoggedFood(loggedFood)
                findNavController().navigateUp() // Go back immediately after logging
            },
            onEdit = { food ->
                val action = LogFoodFragmentDirections.actionLogFoodFragmentToEditFoodFragment(food.id)
                findNavController().navigate(action)
            },
            onDelete = { food ->
                val action =
                    LogFoodFragmentDirections.actionLogFoodFragmentToConfirmDeleteFoodDialogFragment(
                        food.id
                    )
                findNavController().navigate(action)
            }
        )

        b.rvLogFood.adapter = adapter
        b.rvLogFood.layoutManager = LinearLayoutManager(requireContext())

        b.tvCreateCustomFood.setOnClickListener {
            findNavController().navigate(LogFoodFragmentDirections.actionLogFoodFragmentToCreateFoodFragment())
        }

        vm.foods.observe(viewLifecycleOwner) {
            adapter.submitList(it)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _b = null
    }
}
