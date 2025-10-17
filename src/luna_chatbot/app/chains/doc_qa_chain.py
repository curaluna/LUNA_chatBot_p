from __future__ import annotations

from operator import itemgetter
from pathlib import Path
from typing import List, TypedDict


from langchain_core.prompts import MessagesPlaceholder
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from luna_chatbot.app.models import get_llm
from src.luna_chatbot.app.utils.prompts import load_system_prompt, load_developer_prompt
from src.luna_chatbot.app.utils.paths import VECTOR_DIR


class QAInput(TypedDict):
    question: str


def extract_citations(docs: List[Document]) -> str:
    """Turn retrieved docs into concise 'source S.page' citations."""
    parts = []
    for d in docs:
        src = Path(d.metadata.get("source", "unbekannt.pdf")).name
        page = d.metadata.get("page", "?")
        parts.append(f"{src} S.{page}")
    return ", ".join(parts) if parts else "—"


def format_docs(docs: List[Document]) -> str:
    """Pretty-print retrieved docs for the prompt context."""
    chunks = []
    for d in docs:
        src = Path(d.metadata.get("source", "unbekannt.pdf")).name
        page = d.metadata.get("page", "?")
        chunks.append(f"Quelle: {src} (Seite {page})\n{d.page_content}")
    return "\n\n---\n\n".join(chunks)


def build_retriever(
    vector_dir: Path = VECTOR_DIR,
    embedding_model: str = "text-embedding-3-small",
    k: int = 5,
    fetch_k: int = 20,
    use_mmr: bool = True,
    allow_unsafe_deserialization: bool = True,  ##SET TO FALSE
):
    """Create a retriever with sensible defaults."""
    embeddings = OpenAIEmbeddings(model=embedding_model)

    vs = FAISS.load_local(
        str(vector_dir),
        embeddings,
        allow_dangerous_deserialization=allow_unsafe_deserialization,
    )
    search_kwargs = {"k": k, "fetch_k": fetch_k} if use_mmr else {"k": k}
    return vs.as_retriever(
        search_type="mmr" if use_mmr else "similarity",
        search_kwargs=search_kwargs,
    )


def build_prompt() -> ChatPromptTemplate:
    """Compose system + developer prompts and expose context/question slots."""
    system_prompt = load_system_prompt() + load_developer_prompt()
    # Keep ‘Kontext/Frage’ labels if you prefer German in the instructions
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt + "\nKontext Chunks:\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{question}"),
        ]
    )


def build_chain():
    """Return a Runnable that accepts {'question': str} and returns str."""
    retriever = build_retriever()
    prompt = build_prompt()
    llm = get_llm()
    parser = StrOutputParser()

    return (
        RunnablePassthrough.assign(
            context=itemgetter("question") | retriever | RunnableLambda(format_docs)
        )
        | prompt
        | llm
        | parser
    )
