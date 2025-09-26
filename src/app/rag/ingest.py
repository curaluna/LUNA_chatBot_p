from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.app.rag.load_and_chunk import load_pdf, chunk_documents

#paths
try:
    from src.app.paths import PDF_DIR, VECTOR_DIR
except ImportError:
    ROOT = Path(__file__).resolve().parents[3]
    PDF_DIR = ROOT / "data" / "pdfs"
    VECTOR_DIR = ROOT / "data" / "vectorstore"

from dotenv import load_dotenv
load_dotenv()


EMBEDDING_MODEL_NAME = "text-embedding-3-small"

def build_vectorstore():
    """build a FAISS vector store."""
    docs = load_pdf(PDF_DIR)
    chunked_docs = chunk_documents(docs)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
    vs= FAISS.from_documents(chunked_docs, embeddings)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(VECTOR_DIR))
    return VECTOR_DIR


if __name__ == "__main__":
    out = build_vectorstore()
    print(f"Vectorstore saved to {out}")
