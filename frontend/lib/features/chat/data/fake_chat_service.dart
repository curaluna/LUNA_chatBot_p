import "dart:async";

import "../domain/chat_service.dart";

/// A Fake Service to test the UI Streaming-Logic

class FakeChatService implements ChatService {
  @override
  Stream<String> sendMessage(String userMessage, int sessionId) async* {
    var buffer = "";
    final chunks = ["hallo", "mein", "name", "ist", "FAKE-LUNA"];
    for (final chunk in chunks) {
      await Future.delayed(const Duration(milliseconds: 200));
      buffer += " $chunk";
      yield buffer;
    }
  }
}
