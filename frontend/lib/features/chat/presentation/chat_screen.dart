import 'package:flutter/material.dart';
import 'package:luna_assistant_frontend/features/chat/domain/chat_service.dart';
import 'package:luna_assistant_frontend/features/chat/presentation/message_card.dart';

class ChatMessage {
  final String text;
  final bool isUser;

  ChatMessage({required this.text, required this.isUser});
}

class ChatScreen extends StatefulWidget {
  final ChatService chatService;
  final int sessionId;
  const ChatScreen({
    super.key,
    required this.chatService,
    required this.sessionId,
  });

  @override
  State<StatefulWidget> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  // controller for the input form
  final List<ChatMessage> _messages = [];
  final _controller = TextEditingController();

  //Stream + current Message Text
  String _currentStreamText = "";

  //streaming Flag
  bool _isStreaming = false;

  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  void _onSendPressed() {
    final text = _controller.text.trim();

    if (text.isEmpty) return;

    _controller.clear();

    // reset old stream and text
    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
      _isStreaming = true;
      _currentStreamText = "";
    });

    WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());

    widget.chatService
        .sendMessage(text, widget.sessionId)
        .listen(
          (chunk) {
            setState(() {
              _currentStreamText += chunk;
            });
          },
          onDone: () {
            setState(() {
              _isStreaming = false;
              if (_currentStreamText.isNotEmpty) {
                _messages.add(
                  ChatMessage(text: _currentStreamText, isUser: false),
                );
                _currentStreamText = "";
              }
            });
          },
          onError: (error) {
            setState(() {
              _isStreaming = false;
            });
          },
        );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("LUNA Chat")),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              itemCount: _messages.length + (_isStreaming ? 1 : 0),
              itemBuilder: (context, index) {
                if (_isStreaming && index == _messages.length) {
                  return MessageCard(
                    context: context,
                    text: _currentStreamText,
                    isUser: false,
                  );
                }
                final msg = _messages[index];
                return MessageCard(
                  context: context,
                  text: msg.text,
                  isUser: msg.isUser,
                );
              },
            ),
          ),
          _buildInputRow(),
        ],
      ),
    );
  }

  Widget _buildInputRow() {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: "Nachtisch eingeben ...",
              ),
              onSubmitted: (_) => {_onSendPressed()},
            ),
          ),
          const SizedBox(width: 8),
          ElevatedButton(
            onPressed: _isStreaming ? null : _onSendPressed,
            child: const Text("Send"),
          ),
        ],
      ),
    );
  }
}
