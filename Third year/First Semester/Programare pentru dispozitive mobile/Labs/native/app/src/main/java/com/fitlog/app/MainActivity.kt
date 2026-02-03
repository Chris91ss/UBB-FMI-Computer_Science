
package com.fitlog.app
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import com.fitlog.app.databinding.ActivityMainBinding
import androidx.navigation.fragment.NavHostFragment
import android.view.Menu
import android.widget.Toast

class MainActivity : AppCompatActivity() {
  private lateinit var binding: ActivityMainBinding
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    binding = ActivityMainBinding.inflate(layoutInflater)
    setContentView(binding.root)

    setSupportActionBar(binding.toolbar)

    val navHostFragment = supportFragmentManager
        .findFragmentById(R.id.nav_host) as NavHostFragment
    val navController = navHostFragment.navController
    
    val appBarConfiguration = AppBarConfiguration(
        setOf(
            R.id.todaysDiaryFragment
        )
    )
    
    setupActionBarWithNavController(navController, appBarConfiguration)
  }

  // This handles the Up button's functionality from the ActionBar.
  override fun onSupportNavigateUp(): Boolean {
    val navController = findNavController(R.id.nav_host)
    return navController.navigateUp() || super.onSupportNavigateUp()
  }
}
