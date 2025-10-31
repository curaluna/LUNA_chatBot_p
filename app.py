import chainlit as cl
from dotenv import load_dotenv
from src.luna_chatbot.app.agents import agent

load_dotenv()


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


@cl.on_message
async def on_message(msg: cl.Message):
    h_msg = msg.content.strip()
    out = cl.Message(content="")
    async with cl.Step(name="llm", type="llm") as llm_step:
        llm_step.input = h_msg
        out.send()
        async for mode, chunk in agent.astream(
            {"messages": [{"role": "user", "content": h_msg}]},
            stream_mode=["messages", "updates"],
        ):
            if mode == "messages" and "tools" not in chunk:
                content = chunk[0].content
                out.stream_token(content)

            if mode == "updates":
                

                if "tools" in chunk:

