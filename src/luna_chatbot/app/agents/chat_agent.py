from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from luna_chatbot.app.models.chat import base_model
from luna_chatbot.app.tools.rag_tools import get_RAG_data
from luna_chatbot.app.prompts.provider import _pull_system_prompt


async def init_chat_agent():
    return create_agent(
        model=base_model,
        system_prompt=await _pull_system_prompt(),
        tools=[get_RAG_data],
        checkpointer=InMemorySaver(),
    )


# TODO: implement RAG_agents
