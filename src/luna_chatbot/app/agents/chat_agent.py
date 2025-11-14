from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from luna_chatbot.app.models.chat import base_model
from luna_chatbot.app.tools.rag_tools import get_RAG_data
from langsmith import Client

client = Client()
prompt = client.pull_prompt("luna-chatbot-p-system")
print(prompt)
chat_agent = create_agent(
    model=base_model,
    system_prompt=prompt[0].prompt.template,
    tools=[get_RAG_data],
    checkpointer=InMemorySaver(),
)

# TODO: implement RAG_agents
