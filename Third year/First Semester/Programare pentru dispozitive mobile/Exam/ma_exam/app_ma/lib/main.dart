import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() {
  runApp(const MyApp());
}

const String kBaseUrl = 'http://10.0.2.2:2625';
const String kWsUrl = 'ws://10.0.2.2:2625';

// Global stream for WebSocket order notifications
final StreamController<Order> orderNotificationController = StreamController<Order>.broadcast();

class Order {
  final int id;
  final String date;
  final double amount;
  final String type;
  final String category;
  final String description;

  Order({
    required this.id,
    required this.date,
    required this.amount,
    required this.type,
    required this.category,
    required this.description,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'] as int,
      date: json['date'] as String,
      amount: (json['amount'] as num).toDouble(),
      type: json['type'] as String,
      category: json['category'] as String? ?? 'general',
      description: json['description'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'date': date,
      'amount': amount,
      'type': type,
      'category': category,
      'description': description,
    };
  }
}

class OrderApi {
  static const String ordersKey = 'orders_cache';
  static const String allOrdersKey = 'all_orders_cache';

  static Future<List<Order>> getOrders({required bool useCacheOnError}) async {
    debugPrint('[API] GET /orders');
    try {
      final uri = Uri.parse('$kBaseUrl/orders');
      final response = await http.get(uri);
      if (response.statusCode == 200) {
        final List<dynamic> decoded = jsonDecode(response.body) as List<dynamic>;
        final orders = decoded.map((e) => Order.fromJson(e as Map<String, dynamic>)).toList();
        await _saveCache(ordersKey, decoded);
        return orders;
      } else {
        throw Exception('Failed to load orders: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('[API][ERROR] GET /orders failed: $e');
      if (useCacheOnError) {
        final cached = await _readCache(ordersKey);
        if (cached != null) {
          return cached.map((e) => Order.fromJson(e as Map<String, dynamic>)).toList();
        }
      }
      rethrow;
    }
  }

  static Future<Order> getOrderById(int id, {required Order? fallback}) async {
    debugPrint('[API] GET /order/$id');
    try {
      final uri = Uri.parse('$kBaseUrl/order/$id');
      final response = await http.get(uri);
      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body) as Map<String, dynamic>;
        return Order.fromJson(decoded);
      } else {
        throw Exception('Failed to load order: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('[API][ERROR] GET /order/$id failed: $e');
      if (fallback != null) {
        return fallback;
      }
      rethrow;
    }
  }

  static Future<Order> addOrder({
    required String date,
    required String amount,
    required String type,
    required String category,
    required String description,
  }) async {
    debugPrint('[API] POST /order');
    final uri = Uri.parse('$kBaseUrl/order');
    final body = jsonEncode(<String, dynamic>{
      'date': date,
      'amount': double.parse(amount),
      'type': type,
      'category': category,
      'description': description,
    });
    try {
      final response = await http.post(
        uri,
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: body,
      );
      if (response.statusCode == 201) {
        final decoded = jsonDecode(response.body) as Map<String, dynamic>;
        return Order.fromJson(decoded);
      } else {
        throw Exception('Failed to add order: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('[API][ERROR] POST /order failed: $e');
      rethrow;
    }
  }

  static Future<void> deleteOrder(int id) async {
    debugPrint('[API] DELETE /order/$id');
    final uri = Uri.parse('$kBaseUrl/order/$id');
    try {
      final response = await http.delete(uri);
      if (response.statusCode != 200) {
        throw Exception('Failed to delete order: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('[API][ERROR] DELETE /order/$id failed: $e');
      rethrow;
    }
  }

  static Future<List<Order>> getAllOrders({required bool useCacheOnError}) async {
    debugPrint('[API] GET /allOrders');
    try {
      final uri = Uri.parse('$kBaseUrl/allOrders');
      final response = await http.get(uri);
      if (response.statusCode == 200) {
        final List<dynamic> decoded = jsonDecode(response.body) as List<dynamic>;
        final orders = decoded.map((e) => Order.fromJson(e as Map<String, dynamic>)).toList();
        await _saveCache(allOrdersKey, decoded);
        return orders;
      } else {
        throw Exception('Failed to load all orders: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('[API][ERROR] GET /allOrders failed: $e');
      if (useCacheOnError) {
        final cached = await _readCache(allOrdersKey);
        if (cached != null) {
          return cached.map((e) => Order.fromJson(e as Map<String, dynamic>)).toList();
        }
      }
      rethrow;
    }
  }

  static Future<void> _saveCache(String key, List<dynamic> jsonList) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(key, jsonEncode(jsonList));
    debugPrint('[CACHE] Saved $key (${jsonList.length} items)');
  }

  static Future<List<dynamic>?> _readCache(String key) async {
    final prefs = await SharedPreferences.getInstance();
    final value = prefs.getString(key);
    if (value == null) {
      return null;
    }
    try {
      return jsonDecode(value) as List<dynamic>;
    } catch (e) {
      debugPrint('[CACHE][ERROR] Failed to decode cache for $key: $e');
      return null;
    }
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  WebSocketChannel? _channel;
  StreamSubscription? _wsSub;

  @override
  void initState() {
    super.initState();
    _initWebSocket();
  }

  void _initWebSocket() {
    try {
      debugPrint('[WS] Connecting to $kWsUrl');
      _channel = WebSocketChannel.connect(Uri.parse(kWsUrl));
      _wsSub = _channel!.stream.listen(
        (event) {
          debugPrint('[WS] Message: $event');
          final decoded = jsonDecode(event as String) as Map<String, dynamic>;
          final order = Order.fromJson(decoded);
          // Broadcast to listeners (e.g., OrdersListScreen)
          orderNotificationController.add(order);
          // Show snackbar
          final context = navigatorKey.currentContext;
          if (context != null) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  'New order: #${order.id} ${order.category} - \$${order.amount.toStringAsFixed(2)}',
                ),
              ),
            );
          }
        },
        onError: (error) {
          debugPrint('[WS][ERROR] $error');
        },
        onDone: () {
          debugPrint('[WS] Connection closed');
        },
      );
    } catch (e) {
      debugPrint('[WS][ERROR] Failed to connect: $e');
    }
  }

  @override
  void dispose() {
    _wsSub?.cancel();
    _channel?.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restaurant Orders',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      navigatorKey: navigatorKey,
      home: const RootScreen(),
    );
  }
}

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

class RootScreen extends StatefulWidget {
  const RootScreen({super.key});

  @override
  State<RootScreen> createState() => _RootScreenState();
}

class _RootScreenState extends State<RootScreen> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          _index == 0
              ? 'Orders'
              : _index == 1
                  ? 'Reports'
                  : 'Insights',
        ),
      ),
      body: IndexedStack(
        index: _index,
        children: const <Widget>[
          OrdersListScreen(),
          ReportsScreen(),
          InsightsScreen(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _index,
        onTap: (int value) {
          setState(() {
            _index = value;
          });
        },
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.list),
            label: 'Orders',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bar_chart),
            label: 'Reports',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.insights),
            label: 'Insights',
          ),
        ],
      ),
    );
  }
}

class OrdersListScreen extends StatefulWidget {
  const OrdersListScreen({super.key});

  @override
  State<OrdersListScreen> createState() => _OrdersListScreenState();
}

class _OrdersListScreenState extends State<OrdersListScreen> {
  late Future<List<Order>> _future;
  bool _offline = false;
  StreamSubscription<Order>? _orderNotificationSub;

  @override
  void initState() {
    super.initState();
    _load();
    // Listen for WebSocket notifications and auto-refresh
    _orderNotificationSub = orderNotificationController.stream.listen((Order order) {
      debugPrint('[UI] Received WebSocket notification for order #${order.id}, refreshing list');
      _load();
    });
  }

  @override
  void dispose() {
    _orderNotificationSub?.cancel();
    super.dispose();
  }

  void _load() {
    setState(() {
      _offline = false;
      _future = OrderApi.getOrders(useCacheOnError: true).then((value) {
        return value;
      }).catchError((error) {
        debugPrint('[UI][ERROR] Failed to load orders: $error');
        setState(() {
          _offline = true;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load orders: $error')),
        );
        throw error;
      });
    });
  }

  void _deleteOrder(Order order) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Delete order'),
          content: Text('Are you sure you want to delete order #${order.id}?'),
          actions: <Widget>[
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: const Text('Cancel'),
            ),
            FilledButton(
              onPressed: () => Navigator.of(context).pop(true),
              child: const Text('Delete'),
            ),
          ],
        );
      },
    );
    if (confirmed != true) {
      return;
    }
    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return const Center(
          child: CircularProgressIndicator(),
        );
      },
    );
    try {
      await OrderApi.deleteOrder(order.id);
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Order deleted')),
        );
        _load();
      }
    } catch (e) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Delete failed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        if (_offline)
          MaterialBanner(
            content: const Text('Offline - showing last known data.'),
            actions: <Widget>[
              TextButton(
                onPressed: _load,
                child: const Text('Retry'),
              ),
            ],
          ),
        Expanded(
          child: FutureBuilder<List<Order>>(
            future: _future,
            builder: (BuildContext context, AsyncSnapshot<List<Order>> snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      const Text('Error loading orders'),
                      const SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: _load,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                );
              }
              final orders = snapshot.data ?? <Order>[];
              if (orders.isEmpty) {
                return const Center(child: Text('No orders yet.'));
              }
              return ListView.separated(
                itemCount: orders.length,
                separatorBuilder: (BuildContext context, int index) => const Divider(height: 1),
                itemBuilder: (BuildContext context, int index) {
                  final order = orders[index];
                  return ListTile(
                    title: Text('${order.category} - \$${order.amount.toStringAsFixed(2)}'),
                    subtitle: Text('${order.date} • ${order.type}'),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline),
                      onPressed: () => _deleteOrder(order),
                    ),
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute<void>(
                          builder: (BuildContext context) {
                            return OrderDetailScreen(order: order);
                          },
                        ),
                      );
                    },
                  );
                },
              );
            },
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(16),
          child: SizedBox(
            width: double.infinity,
            child: FilledButton.icon(
              onPressed: () async {
                final created = await Navigator.of(context).push<Order?>(
                  MaterialPageRoute<Order?>(
                    builder: (BuildContext context) {
                      return const AddOrderScreen();
                    },
                  ),
                );
                if (created != null) {
                  _load();
                }
              },
              icon: const Icon(Icons.add),
              label: const Text('Add Order'),
            ),
          ),
        ),
      ],
    );
  }
}

class OrderDetailScreen extends StatefulWidget {
  const OrderDetailScreen({super.key, required this.order});

  final Order order;

  @override
  State<OrderDetailScreen> createState() => _OrderDetailScreenState();
}

class _OrderDetailScreenState extends State<OrderDetailScreen> {
  late Future<Order> _future;

  @override
  void initState() {
    super.initState();
    _future = OrderApi.getOrderById(widget.order.id, fallback: widget.order);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Order #${widget.order.id}'),
      ),
      body: FutureBuilder<Order>(
        future: _future,
        builder: (BuildContext context, AsyncSnapshot<Order> snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Failed to load order details: ${snapshot.error}')),
            );
          }
          final order = snapshot.data ?? widget.order;
          return Padding(
            padding: const EdgeInsets.all(16),
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Text(
                      '${order.category} - \$${order.amount.toStringAsFixed(2)}',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    Text('Date: ${order.date}'),
                    Text('Type: ${order.type}'),
                    Text('Category: ${order.category}'),
                    const SizedBox(height: 8),
                    Text(
                      'Description:',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 4),
                    Text(order.description.isEmpty ? 'No description' : order.description),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class AddOrderScreen extends StatefulWidget {
  const AddOrderScreen({super.key});

  @override
  State<AddOrderScreen> createState() => _AddOrderScreenState();
}

class _AddOrderScreenState extends State<AddOrderScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _dateController = TextEditingController();
  final TextEditingController _amountController = TextEditingController();
  final TextEditingController _typeController = TextEditingController();
  final TextEditingController _categoryController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();

  bool _submitting = false;

  @override
  void dispose() {
    _dateController.dispose();
    _amountController.dispose();
    _typeController.dispose();
    _categoryController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }
    setState(() {
      _submitting = true;
    });
    try {
      final order = await OrderApi.addOrder(
        date: _dateController.text.trim(),
        amount: _amountController.text.trim(),
        type: _typeController.text.trim(),
        category: _categoryController.text.trim(),
        description: _descriptionController.text.trim(),
      );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Order created')),
        );
        Navigator.of(context).pop(order);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to create order: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _submitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Order'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: <Widget>[
              TextFormField(
                controller: _dateController,
                decoration: const InputDecoration(
                  labelText: 'Date (YYYY-MM-DD)',
                  border: OutlineInputBorder(),
                ),
                validator: (String? value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter date';
                  }
                  if (!RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(value)) {
                    return 'Use format YYYY-MM-DD';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _amountController,
                decoration: const InputDecoration(
                  labelText: 'Amount',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                validator: (String? value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter amount';
                  }
                  final parsed = double.tryParse(value);
                  if (parsed == null || parsed <= 0) {
                    return 'Enter a positive number';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _typeController,
                decoration: const InputDecoration(
                  labelText: 'Type (dine-in, takeout, delivery)',
                  border: OutlineInputBorder(),
                ),
                validator: (String? value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter type';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _categoryController,
                decoration: const InputDecoration(
                  labelText: 'Category (pizza, sushi, burger, ...)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description',
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _submitting ? null : _submit,
                  child: _submitting
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Save'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key});

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  late Future<List<_MonthlyTotal>> _future;
  bool _offline = false;
  StreamSubscription<Order>? _orderNotificationSub;

  @override
  void initState() {
    super.initState();
    _load();
    // Listen for WebSocket notifications and auto-refresh
    _orderNotificationSub = orderNotificationController.stream.listen((Order order) {
      debugPrint('[UI] Reports: Received WebSocket notification for order #${order.id}, refreshing');
      _load();
    });
  }

  @override
  void dispose() {
    _orderNotificationSub?.cancel();
    super.dispose();
  }

  void _load() {
    setState(() {
      _offline = false;
      _future = OrderApi.getAllOrders(useCacheOnError: true).then((List<Order> orders) {
        final Map<String, double> totals = <String, double>{};
        for (final Order o in orders) {
          final String key = o.date.substring(0, 7);
          totals[key] = (totals[key] ?? 0) + o.amount;
        }
        final List<_MonthlyTotal> list = totals.entries
            .map((MapEntry<String, double> e) => _MonthlyTotal(month: e.key, total: e.value))
            .toList();
        list.sort((_MonthlyTotal a, _MonthlyTotal b) => b.total.compareTo(a.total));
        return list;
      }).catchError((Object error) {
        debugPrint('[UI][ERROR] Reports load failed: $error');
        setState(() {
          _offline = true;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load reports: $error')),
        );
        throw error;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        if (_offline)
          MaterialBanner(
            content: const Text('Offline - showing last known data.'),
            actions: <Widget>[
              TextButton(
                onPressed: _load,
                child: const Text('Retry'),
              ),
            ],
          ),
        Expanded(
          child: FutureBuilder<List<_MonthlyTotal>>(
            future: _future,
            builder: (BuildContext context, AsyncSnapshot<List<_MonthlyTotal>> snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      const Text('Error loading reports'),
                      const SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: _load,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                );
              }
              final List<_MonthlyTotal> data = snapshot.data ?? <_MonthlyTotal>[];
              if (data.isEmpty) {
                return const Center(child: Text('No data available.'));
              }
              return ListView.builder(
                itemCount: data.length,
                itemBuilder: (BuildContext context, int index) {
                  final _MonthlyTotal item = data[index];
                  return ListTile(
                    leading: CircleAvatar(
                      child: Text('${index + 1}'),
                    ),
                    title: Text(item.month),
                    trailing: Text('\$${item.total.toStringAsFixed(2)}'),
                  );
                },
              );
            },
          ),
        ),
      ],
    );
  }
}

class _MonthlyTotal {
  _MonthlyTotal({required this.month, required this.total});

  final String month;
  final double total;
}

class InsightsScreen extends StatefulWidget {
  const InsightsScreen({super.key});

  @override
  State<InsightsScreen> createState() => _InsightsScreenState();
}

class _InsightsScreenState extends State<InsightsScreen> {
  late Future<List<_CategoryTotal>> _future;
  bool _offline = false;
  StreamSubscription<Order>? _orderNotificationSub;

  @override
  void initState() {
    super.initState();
    _load();
    // Listen for WebSocket notifications and auto-refresh
    _orderNotificationSub = orderNotificationController.stream.listen((Order order) {
      debugPrint('[UI] Insights: Received WebSocket notification for order #${order.id}, refreshing');
      _load();
    });
  }

  @override
  void dispose() {
    _orderNotificationSub?.cancel();
    super.dispose();
  }

  void _load() {
    setState(() {
      _offline = false;
      _future = OrderApi.getAllOrders(useCacheOnError: true).then((List<Order> orders) {
        final Map<String, double> totals = <String, double>{};
        for (final Order o in orders) {
          final String key = o.category;
          totals[key] = (totals[key] ?? 0) + o.amount;
        }
        final List<_CategoryTotal> list = totals.entries
            .map((MapEntry<String, double> e) => _CategoryTotal(category: e.key, total: e.value))
            .toList();
        list.sort((_CategoryTotal a, _CategoryTotal b) => b.total.compareTo(a.total));
        if (list.length > 3) {
          return list.sublist(0, 3);
        }
        return list;
      }).catchError((Object error) {
        debugPrint('[UI][ERROR] Insights load failed: $error');
        setState(() {
          _offline = true;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load insights: $error')),
        );
        throw error;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        if (_offline)
          MaterialBanner(
            content: const Text('Offline - showing last known data.'),
            actions: <Widget>[
              TextButton(
                onPressed: _load,
                child: const Text('Retry'),
              ),
            ],
          ),
        Expanded(
          child: FutureBuilder<List<_CategoryTotal>>(
            future: _future,
            builder: (BuildContext context, AsyncSnapshot<List<_CategoryTotal>> snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      const Text('Error loading insights'),
                      const SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: _load,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                );
              }
              final List<_CategoryTotal> data = snapshot.data ?? <_CategoryTotal>[];
              if (data.isEmpty) {
                return const Center(child: Text('No data available.'));
              }
              return ListView.builder(
                itemCount: data.length,
                itemBuilder: (BuildContext context, int index) {
                  final _CategoryTotal item = data[index];
                  return ListTile(
                    leading: CircleAvatar(
                      child: Text('${index + 1}'),
                    ),
                    title: Text(item.category),
                    trailing: Text('\$${item.total.toStringAsFixed(2)}'),
                  );
                },
              );
            },
          ),
        ),
      ],
    );
  }
}

class _CategoryTotal {
  _CategoryTotal({required this.category, required this.total});

  final String category;
  final double total;
}
