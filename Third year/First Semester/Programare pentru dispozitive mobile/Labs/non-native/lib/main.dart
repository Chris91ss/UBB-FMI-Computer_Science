import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'repository/fitlog_repository.dart';
import 'repository/fitlog_server_repository.dart';
import 'screens/diary_screen.dart';
import 'state/fitlog_model.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  // Create local repository for offline fallback
  final localRepository = FitLogRepository();
  // Wrap with server repository (falls back to local if server unavailable)
  // Note: For Android emulator, use 'http://10.0.2.2:3000'
  //       For iOS simulator, use 'http://localhost:3000'
  //       For physical device, use your computer's IP (e.g., 'http://192.168.1.100:3000')
  final serverRepository = FitLogServerRepository(
    localRepository: localRepository,
    serverUrl: 'http://10.0.2.2:3000', // Android emulator uses 10.0.2.2 for host machine
  );
  runApp(
    ChangeNotifierProvider(
      create: (_) => FitLogModel(repository: serverRepository),
      child: const FitLogApp(),
    ),
  );
}

class FitLogApp extends StatelessWidget {
  const FitLogApp({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.light,
    );
    return MaterialApp(
      title: 'FitLog',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: colorScheme,
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF6F6F6),
      ),
      home: const DiaryScreen(),
    );
  }
}
