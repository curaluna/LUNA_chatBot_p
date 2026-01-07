from dotenv import load_dotenv

from langchain_core.messages import AIMessageChunk

load_dotenv()


async def agent_call(prompt: str, sessionId: int, chat_agent):
    async for step in chat_agent.astream(
        {"messages": [{"role": "user", "content": prompt}]},
        {"configurable": {"thread_id": sessionId}},
        stream_mode=["messages", "updates"],
    ):
        if isinstance(step, tuple):
            mode, chunk = step

            

            if mode == "messages":
                if isinstance(chunk[0], AIMessageChunk):
                    print("MESSAGE_CHUNK: ",chunk[0].content)
                    yield chunk[0].content
            if mode == "updates":
                print("UPDATE_CHUNK: ", chunk)
