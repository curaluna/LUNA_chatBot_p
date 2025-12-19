import 'dart:math';
import 'package:flutter/material.dart';

import 'package:luna_assistant_frontend/features/chat/data/http_chat_service.dart';
import 'package:luna_assistant_frontend/features/chat/domain/chat_service.dart';
import 'package:luna_assistant_frontend/features/chat/presentation/chat_screen.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    await dotenv.load(fileName: ".env");
  } catch (e) {
    throw Exception('Error loading .env file: $e');
  }

  final int sessionId = Random().nextInt(1000);
  final ChatService chatService = HttpChatService(sessionId: sessionId);
  runApp(MyApp(chatService: chatService, sessionId: sessionId));
}

class MyApp extends StatelessWidget {
  final ChatService chatService;
  final int sessionId;

  const MyApp({super.key, required this.chatService, required this.sessionId});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.from(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.lightBlue,
          brightness: Brightness.dark,
        ),
        textTheme: TextTheme(displayMedium: TextStyle(color: Colors.white30)),
      ),
      home: ChatScreen(chatService: chatService, sessionId: sessionId),
    );
  }
}
