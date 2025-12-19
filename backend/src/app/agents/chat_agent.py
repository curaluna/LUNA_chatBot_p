from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

from app.models.chat import base_model
from app.tools.rag_tools import get_RAG_data
from app.prompts.provider import _pull_system_prompt


async def init_chat_agent(conn: AsyncConnection):
    """
    Initialisiert den Agenten mit einer bestehenden DB-Verbindung für Checkpoints.
    """

    # 1. Saver erstellen
    checkpointer = AsyncPostgresSaver(conn)

    # 2. Sicherstellen, dass die Checkpoint-Tabellen existieren
    # (Dies muss einmal beim Start passieren)
    await checkpointer.setup()

    # 3. Agent erstellen (Modern React Style)
    agent = create_agent(
        model=base_model,
        tools=[get_RAG_data],
        system_prompt=await _pull_system_prompt(),
        checkpointer=checkpointer,
    )

    return agent
