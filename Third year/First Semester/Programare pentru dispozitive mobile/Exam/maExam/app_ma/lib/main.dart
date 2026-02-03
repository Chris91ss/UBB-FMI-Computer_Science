import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'models/sale.dart';
import 'services/websocket_service.dart';
import 'services/connectivity_service.dart';
import 'screens/sales_list_screen.dart';
import 'screens/reports_screen.dart';
import 'screens/insights_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await ConnectivityService.initialize();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Real Estate Sales',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final Logger _logger = Logger();
  final WebSocketService _webSocketService = WebSocketService();
  int _currentIndex = 0;

  // GlobalKeys to access each screen's state for refreshing
  final GlobalKey<SalesListScreenState> _salesListKey = GlobalKey();
  final GlobalKey<ReportsScreenState> _reportsKey = GlobalKey();
  final GlobalKey<InsightsScreenState> _insightsKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    _initWebSocket();
  }

  void _initWebSocket() {
    _logger.i('MainScreen: Initializing WebSocket connection');
    _webSocketService.connect();
    
    _webSocketService.onNewSale.listen((sale) {
      _logger.i('MainScreen: Received new sale notification: $sale');
      _showNewSaleNotification(sale);
    });
  }

  void _showNewSaleNotification(Sale sale) {
    if (!mounted) return;

    // Auto-refresh the sales list when a new sale is received
    _salesListKey.currentState?.refresh();

    // Show snackbar notification (non-blocking)
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'New ${sale.type}: ${sale.category} - \$${sale.amount.toStringAsFixed(2)}',
        ),
        backgroundColor: Colors.green,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  @override
  void dispose() {
    _logger.i('MainScreen: Disposing WebSocket connection');
    _webSocketService.dispose();
    super.dispose();
  }

  void _onTabChanged(int index) {
    setState(() => _currentIndex = index);
    
    // Refresh the selected tab's data
    switch (index) {
      case 0:
        _salesListKey.currentState?.refresh();
        break;
      case 1:
        _reportsKey.currentState?.refresh();
        break;
      case 2:
        _insightsKey.currentState?.refresh();
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: [
          SalesListScreen(key: _salesListKey),
          ReportsScreen(key: _reportsKey),
          InsightsScreen(key: _insightsKey),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: _onTabChanged,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Sales',
          ),
          NavigationDestination(
            icon: Icon(Icons.analytics_outlined),
            selectedIcon: Icon(Icons.analytics),
            label: 'Reports',
          ),
          NavigationDestination(
            icon: Icon(Icons.insights_outlined),
            selectedIcon: Icon(Icons.insights),
            label: 'Insights',
          ),
        ],
      ),
    );
  }
}
