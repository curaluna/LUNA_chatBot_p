from langchain_core.messages import AIMessageChunk


def isAIMessage(chunk: tuple):
    return isinstance(chunk[0], AIMessageChunk)
