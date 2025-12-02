abstract class ChatService {
  //Take a user message and return a stream of api text chunks
  Stream<String> sendMessage(String userMessage, int sessionId);
}
