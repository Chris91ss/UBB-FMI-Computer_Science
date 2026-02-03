package com.fitlog.app.ui.dialogs

import android.app.Dialog
import android.os.Bundle
import androidx.fragment.app.DialogFragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.navArgs
import com.fitlog.app.R
import com.fitlog.app.vm.MainViewModel
import com.google.android.material.dialog.MaterialAlertDialogBuilder

class ConfirmRemoveLoggedFoodDialogFragment : DialogFragment() {
    private val args: ConfirmRemoveLoggedFoodDialogFragmentArgs by navArgs()
    private val vm: MainViewModel by activityViewModels()

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        return MaterialAlertDialogBuilder(requireContext())
            .setTitle("Remove food?")
            .setMessage("This will remove the food from your diary for today. This cannot be undone.")
            .setNegativeButton(R.string.cancel, null)
            .setPositiveButton("Remove") { _, _ ->
                vm.deleteLoggedFood(args.loggedFoodId)
            }
            .create()
    }
}
