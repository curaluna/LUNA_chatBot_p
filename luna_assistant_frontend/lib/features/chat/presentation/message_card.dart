import 'package:flutter/material.dart';

class MessageCard extends StatelessWidget {
  const MessageCard({
    super.key,
    required this.context,
    required this.text,
    required this.isUser,
  });
  final BuildContext context;
  final String text;
  final bool isUser;

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * .75,
        ),
        child: Container(
          margin: EdgeInsets.all(16),
          padding: EdgeInsets.all(10),
          decoration: BoxDecoration(
            boxShadow: [
              BoxShadow(
                color: !isUser ? Colors.teal[200]! : Colors.amber[600]!,
                offset: Offset.zero,
                blurRadius: 1,
                spreadRadius: 1,
              ),
            ],
            color: isUser ? Colors.teal[200] : Colors.amber[600],
            borderRadius: BorderRadius.all(Radius.circular(16)),
            border: Border.all(color: Colors.black),
          ),
          child: text == ""
              ? SizedBox.fromSize(
                  size: Size(20, 20),
                  child: CircularProgressIndicator(color: Colors.black45),
                )
              : Text(
                  text,
                  style: TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.w500,
                  ),
                ),
        ),
      ),
    );
  }
}
