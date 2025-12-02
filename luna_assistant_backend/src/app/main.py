from app.utils import env_loader
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.agents.chat_agent import init_chat_agent
from app.services.chat_service import agent_call
import logging


env_loader

logger = logging.getLogger(__name__)
logging.basicConfig(filename="myapp.log", level=logging.INFO)

chat_agents: any


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chat_agents
    logger.info("System started")
    chat_agents = await init_chat_agent()
    logger.info("Created chat_agent")
    yield
    logger.info("Clearing chat_agent")
    chat_agents.clear()
    logger.info("Stopping system")


app = FastAPI(lifespan=lifespan)


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
    sessionId: int


@app.post("/chat")
def root(body: ChatRequest):
    global chat_agents
    return StreamingResponse(
        agent_call(body.message, body.sessionId, chat_agents), media_type="application/json"
    )
