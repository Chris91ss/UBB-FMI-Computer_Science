import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:logger/logger.dart';

class ConnectivityService {
  static final Logger _logger = Logger();
  static final Connectivity _connectivity = Connectivity();
  
  static final StreamController<bool> _connectionController = 
      StreamController<bool>.broadcast();
  
  static Stream<bool> get onConnectivityChanged => _connectionController.stream;
  static bool _isOnline = true;
  static bool get isOnline => _isOnline;

  static StreamSubscription<ConnectivityResult>? _subscription;

  static Future<void> initialize() async {
    _logger.i('ConnectivityService: Initializing');
    
    // Check initial connectivity
    final result = await _connectivity.checkConnectivity();
    _updateConnectionStatus(result);
    
    // Listen for changes
    _subscription = _connectivity.onConnectivityChanged.listen(_updateConnectionStatus);
  }

  static void _updateConnectionStatus(ConnectivityResult result) {
    final wasOnline = _isOnline;
    _isOnline = result != ConnectivityResult.none;
    
    _logger.i('ConnectivityService: Connection status: $_isOnline (was: $wasOnline)');
    
    if (wasOnline != _isOnline) {
      _connectionController.add(_isOnline);
    }
  }

  static Future<bool> checkConnectivity() async {
    final result = await _connectivity.checkConnectivity();
    _isOnline = result != ConnectivityResult.none;
    _logger.i('ConnectivityService: Manual check - isOnline: $_isOnline');
    return _isOnline;
  }

  static void dispose() {
    _subscription?.cancel();
    _connectionController.close();
  }
}
