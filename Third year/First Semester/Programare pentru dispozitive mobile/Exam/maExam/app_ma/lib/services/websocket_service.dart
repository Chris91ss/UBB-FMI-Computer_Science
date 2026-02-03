import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:logger/logger.dart';
import '../models/sale.dart';

class WebSocketService {
  static const String wsUrl = 'ws://10.0.2.2:2626'; // Android emulator localhost
  static final Logger _logger = Logger();
  
  WebSocketChannel? _channel;
  final StreamController<Sale> _saleController = StreamController<Sale>.broadcast();
  bool _isConnected = false;

  Stream<Sale> get onNewSale => _saleController.stream;
  bool get isConnected => _isConnected;

  void connect() {
    if (_isConnected) {
      _logger.w('WebSocket: Already connected');
      return;
    }

    _logger.i('WebSocket: Connecting to $wsUrl');
    try {
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
      _isConnected = true;
      _logger.i('WebSocket: Connected successfully');

      _channel!.stream.listen(
        (message) {
          _logger.i('WebSocket: Received message: $message');
          try {
            final data = json.decode(message);
            final sale = Sale.fromJson(data);
            _logger.i('WebSocket: Parsed new sale: $sale');
            _saleController.add(sale);
          } catch (e) {
            _logger.e('WebSocket: Error parsing message: $e');
          }
        },
        onError: (error) {
          _logger.e('WebSocket: Error: $error');
          _isConnected = false;
          _reconnect();
        },
        onDone: () {
          _logger.i('WebSocket: Connection closed');
          _isConnected = false;
          _reconnect();
        },
      );
    } catch (e) {
      _logger.e('WebSocket: Connection error: $e');
      _isConnected = false;
      _reconnect();
    }
  }

  void _reconnect() {
    Future.delayed(const Duration(seconds: 5), () {
      if (!_isConnected) {
        _logger.i('WebSocket: Attempting to reconnect...');
        connect();
      }
    });
  }

  void disconnect() {
    _logger.i('WebSocket: Disconnecting');
    _channel?.sink.close();
    _isConnected = false;
  }

  void dispose() {
    _logger.i('WebSocket: Disposing');
    disconnect();
    _saleController.close();
  }
}
