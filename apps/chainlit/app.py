import chainlit as cl
from dotenv import load_dotenv

import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # -> Projektroot
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.chains.doc_qa_chain import doc_qa_chain, retriever, extract_citations  # <- neu

load_dotenv()

@cl.on_message
async def on_message(message: cl.Message):
    user_q = message.content.strip()
    if not user_q:
        await cl.Message(content="Bitte gib eine Frage ein.").send()
        return

    # 1) Kontext holen (zeigt dir, was wirklich benutzt wird)
    docs = await retriever.aget_relevant_documents(user_q)
    cites = extract_citations(docs)
    await cl.Message(content=f"_Kontextquellen:_ {cites}").send()  # Debug/Transparenz

    # 2) Antwort aus der RAG-Chain
    answer = await doc_qa_chain.ainvoke({"question": user_q})
    await cl.Message(content=answer).send()