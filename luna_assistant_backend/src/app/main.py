import logging
from contextlib import asynccontextmanager


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Ensure env vars are loaded first
import app.utils.env_loader
from app.agents.chat_agent import init_chat_agent
from app.data.database import get_checkpointer_conn
from app.services.chat_service import agent_call

# Configure Logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="myapp.log", level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that handles the database connection for the agent's memory.
    1. Opens a persistent connection to Postgres (Cloud SQL).
    2. Initializes the Agent with that connection.
    3. Stores the agent in 'app.state' for endpoints to use.
    4. Closes the connection on shutdown.
    """
    logger.info("System starting up...")

    # 1. Get the Checkpointer Connection Context
    # This creates the Psycopg3 connection required by LangGraph
    conn_ctx = get_checkpointer_conn()

    # 2. Manually enter the context to keep the connection open for the whole app life
    db_conn = await conn_ctx.__aenter__()

    try:
        logger.info("Initializing Chat Agent with Persistence...")

        # 3. Initialize Agent and store in app.state
        # We pass the open DB connection to the agent factory
        app.state.agent = await init_chat_agent(db_conn)

        logger.info("Chat Agent Ready.")
        yield

    finally:
        logger.info("Shutting down system...")

        # 4. Cleanup: Close the database connection
        # This ensures we don't leak connections on Cloud SQL
        await conn_ctx.__aexit__(None, None, None)
        logger.info("Database connection closed.")


app = FastAPI(lifespan=lifespan)

# CORS Setup
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    sessionId: str


@app.post("/chat")
async def root(request: Request, body: ChatRequest):
    """
    Chat Endpoint.
    Retrieves the initialized agent from 'request.app.state.agent'.
    """
    # 1. Get the agent from the app state (initialized in lifespan)
    # This replaces the global 'chat_agents' variable
    agent = request.app.state.agent

    # 2. Pass the agent instance to your service logic
    return StreamingResponse(
        agent_call(body.message, body.sessionId, agent), media_type="application/json"
    )
