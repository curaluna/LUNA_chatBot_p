from langchain import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from models import base_model
from tools import load_system_prompt, get_RAG_info


chat_agent = create_agent(
    model=base_model,
    system_prompt=load_system_prompt(),
    tools=get_RAG_info,
    checkpointer=InMemorySaver(),
)

# TODO: implement RAG_agent
