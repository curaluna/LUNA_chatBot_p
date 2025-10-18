import uuid
import chainlit as cl
from dotenv import load_dotenv
import os, sys
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from luna_chatbot.app.chains.doc_qa_chain import (
    build_chain,
    build_retriever,
    extract_citations,
)

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


@cl.on_chat_start
async def on_chat_start():
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)

    history_store = {}

    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in history_store:
            history_store[session_id] = InMemoryChatMessageHistory()
        return history_store[session_id]

    chain_with_history = RunnableWithMessageHistory(
        build_chain(),
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    cl.user_session.set("chain", chain_with_history)
    retriever = build_retriever()
    cl.user_session.set("retriever", retriever)


@cl.on_message
async def on_message(message: cl.Message):
    user_q = message.content.strip()

    if not user_q:
        await cl.Message(content="Bitte geben Sie eine Frage ein.").send()
        return

    chain = cl.user_session.get("chain")
    session_id = cl.user_session.get("session_id")
    retriever = cl.user_session.get("retriever")

    docs = await retriever.aget_relevant_documents(user_q)
    cites = extract_citations(docs)
    await cl.Message(content="Chunks used in Kontext: \n" + cites + "\n\n").send()
    # STREAMING ANSWER
    out = cl.Message(content="")
    await out.send()

    async for event in chain.astream(
        {"question": user_q}, config={"configurable": {"session_id": session_id}}
    ):
        chunk = (
            event
            if isinstance(event, str)
            else (
                event.get("output_text")
                or event.get("answer")
                or event.get("content")
                or event.get("text")
            )
        )

        if chunk:
            await out.stream_token(chunk)

        await out.update()
