package com.fitlog.app.ui.dialogs

import android.app.Dialog
import android.os.Bundle
import androidx.fragment.app.DialogFragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.navArgs
import com.fitlog.app.R
import com.fitlog.app.vm.MainViewModel
import com.google.android.material.dialog.MaterialAlertDialogBuilder

class ConfirmDeleteFoodDialogFragment : DialogFragment() {
    private val args: ConfirmDeleteFoodDialogFragmentArgs by navArgs()
    private val vm: MainViewModel by activityViewModels()

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        return MaterialAlertDialogBuilder(requireContext())
            .setTitle("Delete food?")
            .setMessage("This will permanently remove the food from your list. This cannot be undone.")
            .setNegativeButton(R.string.cancel, null)
            .setPositiveButton(R.string.delete) { _, _ ->
                vm.deleteFood(args.foodId)
            }
            .create()
    }
}
