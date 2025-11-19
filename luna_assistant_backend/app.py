import chainlit as cl
from chainlit.types import ThreadDict, Dict, Optional
from dotenv import load_dotenv
from luna_chatbot.app.agents.chat_agent import init_chat_agent
from luna_chatbot.app.utils.type_helpers import isAIMessage


load_dotenv()


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    return default_user


@cl.on_chat_start
async def on_chat_start():
    global chat_agent
    chat_agent = await init_chat_agent()


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Entlastung für Angehörige",
            message=(
                "Ich pflege einen Angehörigen und brauche schnelle, passende Entlastungsangebote in meiner Nähe."
            ),
            icon="/public/care.svg",
        ),
        cl.Starter(
            label="Demenzbetreuung – Alltag strukturieren",
            message=(
                "Hilf mir, eine einfache, alltagsnahe Tagesstruktur für Demenzbetreuung zu erstellen."
            ),
            icon="/public/brain.svg",
        ),
        cl.Starter(
            label="Sturzprophylaxe zuhause",
            message=(
                "Erstelle einen kompakten Plan zur Sturzprävention mit kurzer Checkliste und einfachen Übungen."
            ),
            icon="/public/shield.svg",
        ),
    ]


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")


@cl.on_message
async def on_message(user_msg: cl.Message):
    out_msg = cl.Message(content="")

    async with cl.Step(type="llm") as run_chat:
        # combined stream with "messages" and "update" token
        run_chat.input = user_msg.content

        async for mode, chunk in chat_agent.astream(
            {"messages": [{"role": "user", "content": user_msg.content}]},
            {"configurable": {"thread_id": cl.user_session.get("id")}},
            stream_mode=["messages", "updates", "debug"],
        ):
            if mode == "messages" and isAIMessage(chunk):
                token, metadata = chunk

                content = chunk[0].content
                await out_msg.stream_token(content)
            if mode == "updates":
                # if its a toolcall show tool name tool input and tool output
                if "tools" in chunk:
                    # call a child step if its a tool call
                    async with cl.Step(
                        name=chunk["tools"]["messages"][0].name
                    ) as tool_step:
                        tool_step.input = run_chat.input
                        tool_step.output = chunk["tools"]["messages"][0].content

                # if its a modelcall show in and output
                if "model" in chunk:
                    run_chat.output = chunk["model"]["messages"][0].content

            # if mode == "debug":
            #    print(f"Step: {chunk['step']}", end="\n")
            #    print(f"Type: {chunk['type']}-{chunk['payload']['name']}", end="\n")
            #    print(f"Timestamp: {chunk['timestamp']}", end="\n\n")
            # if nessecary add additional debug information

    await out_msg.send()
    await out_msg.update()
