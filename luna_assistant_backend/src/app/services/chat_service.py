from dotenv import load_dotenv

load_dotenv()


async def agent_call(prompt: str, sessionId: int, chat_agent):
    async for step in chat_agent.astream(
        {"messages": [{"role": "user", "content": prompt}]},
        {"configurable": {"thread_id": sessionId}},
        stream_mode=["messages", "updates"],
    ):
        if isinstance(step, tuple):
            mode, chunk = step

            print("Mode: ", mode)

            if mode == "messages":
                yield chunk[0].content
            if mode == "updates":
                print("Chunk: ", chunk)
