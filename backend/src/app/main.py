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

   
    conn_ctx = get_checkpointer_conn()

   
    app.state.db_conn = await conn_ctx.__aenter__()

    try:
        logger.info("Initializing Chat Agent with Persistence...")

        app.state.agent = await init_chat_agent(app.state.db_conn)

        logger.info("Chat Agent Ready.")
        yield

    finally:
        logger.info("Shutting down system...")

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
   
    #reinitializes the agent to refetch the prompts
    old_agent = request.app.state.agent
    old_agent.close() 
    request.app.state.agent = await init_chat_agent(request.app.state.db_conn)
    agent =  request.app.state.agent
   
    return StreamingResponse(
        agent_call(body.message, body.sessionId, agent), media_type="application/json"
    )
