import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/chat_service.dart';

class HttpChatService implements ChatService {
  static const String backendBaseUrl = String.fromEnvironment(
    'BACKEND_BASE_URL',
    defaultValue: 'http://localhost:1000',
  );
  late final Uri endpoint = Uri.parse('$backendBaseUrl/chat');
  final http.Client client = http.Client();
  final int sessionId;

  HttpChatService({required this.sessionId});

  @override
  Stream<String> sendMessage(String userMessage, int sessionId) async* {
    //prepare request
    final request = http.Request("POST", endpoint);
    request.headers["Content-Type"] = "application/json";
    request.body = jsonEncode({
      "message": userMessage,
      "sessionId": this.sessionId.toString(),
    });

    try {
      //send request
      final streamedResponse = await client.send(request);

      //check response for statuscodes
      if (streamedResponse.statusCode != 200) {
        throw Exception("Backend Error ${streamedResponse.statusCode}");
      }
      final byteStream = streamedResponse.stream;
      final textStream = byteStream.transform(utf8.decoder);

      await for (final chunk in textStream) {
        yield chunk;
      }
    } catch (e) {
      throw Exception(e.hashCode);
    }
  }
}
