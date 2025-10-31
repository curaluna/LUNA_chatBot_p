from langchain_openai import ChatOpenAI


basic_model = ChatOpenAI(
    model="gpt-5-mini", temperature=0.3, reasoning_effort="minimal"
)

# TODO: implement RAG model for more effective rag retrieval
rag_model = ChatOpenAI(model="")
