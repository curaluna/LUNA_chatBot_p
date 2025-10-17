from langchain_openai import ChatOpenAI

MODEL_NAME = "gpt-5-nano-2025-08-07"
TEMPERATURE = 0.4
STREAMING = True


def get_llm(
    model_name=MODEL_NAME, temperature=TEMPERATURE, streaming=STREAMING
) -> ChatOpenAI:
    """Initialize and return a ChatOpenAI model with specified parameters."""
    return ChatOpenAI(model=model_name, temperature=temperature, streaming=streaming)
