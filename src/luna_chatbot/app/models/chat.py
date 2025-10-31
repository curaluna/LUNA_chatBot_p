from langchain_openai import ChatOpenAI


base_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# TODO: implement RAG model for more effective rag retrieval
rag_model = ChatOpenAI(model="")
