import 'dart:math';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:luna_assistant_frontend/features/chat/data/http_chat_service.dart';
import 'package:luna_assistant_frontend/features/chat/domain/chat_service.dart';
import 'package:luna_assistant_frontend/features/chat/presentation/chat_screen.dart';

void main() {
  final http.Client client = http.Client();
  final Uri endpoint = Uri(host: "127.0.0.1", port: 8000, path: 'chat');
  final int sessionId = Random().nextInt(1000);
  final ChatService chatService = HttpChatService(
    client: client,
    endpoint: endpoint,
    sessionId: sessionId,
  );
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
          seedColor: Colors.amber,
          brightness: Brightness.dark,
        ),
        textTheme: TextTheme(displayMedium: TextStyle(color: Colors.white30)),
      ),
      home: ChatScreen(chatService: chatService, sessionId: sessionId),
    );
  }
}
