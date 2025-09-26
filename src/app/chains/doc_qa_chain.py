from pathlib import Path
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnableLambda
from src.app.models import get_llm
from src.app.prompts import SYSTEM_PROMPT

# Pfad zum gespeicherten VectorStore
try:
    from src.app.paths import VECTOR_DIR
except Exception:
    VECTOR_DIR = Path(__file__).resolve().parents[3] / "data" / "vectorstore"

from typing import List
from langchain.schema import Document

def extract_citations(docs: List[Document]) -> str:
    from pathlib import Path
    parts = []
    for d in docs:
        src = Path(d.metadata.get("source", "unbekannt.pdf")).name
        page = d.metadata.get("page", "?")
        parts.append(f"{src} S.{page}")
    return ", ".join(parts) if parts else "—"


# --- Retriever laden ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vs = FAISS.load_local(str(VECTOR_DIR), embeddings, allow_dangerous_deserialization=True)
retriever = vs.as_retriever(search_kwargs={"k": 4})

# Kontext hübsch formatieren
def format_docs(docs):
    parts = []
    for d in docs:
        src = Path(d.metadata.get("source", "unbekannt.pdf")).name
        page = d.metadata.get("page", "?")
        parts.append(f"Quelle: {src} (Seite {page})\n{d.page_content}")
    return "\n\n---\n\n".join(parts)

def get_question(x):  # erwartet {"question": "..."}
    return x["question"]

# Prompt: System-Regeln + Frage + Kontext
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT + 
     "\nNutze ausschließlich den bereitgestellten Kontext. "
     "Wenn kein passender Kontext vorhanden ist, antworte: 'Kein relevanter Kontext gefunden.'"),
    ("user", "Frage: {question}\n\nKontext:\n{context}")
])

llm = get_llm()
parser = StrOutputParser()

# LCEL: Frage -> Retriever -> Kontext -> Prompt -> LLM -> Parser
doc_qa_chain = (
    {
        "context": RunnableLambda(get_question) | retriever | RunnableLambda(format_docs),
        "question": RunnableLambda(get_question),
    }
    | prompt
    | llm
    | parser
)