from langchain_openai import ChatOpenAI

MODEL_NAME = "gpt-5-nano"
TEMPERATURE = 0.3


def get_llm(model_name=MODEL_NAME, temperature=TEMPERATURE) -> ChatOpenAI:
    """Initialize and return a ChatOpenAI model with specified parameters."""
    return ChatOpenAI(model=model_name, temperature=temperature)