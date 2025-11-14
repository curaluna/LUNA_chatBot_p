from pathlib import Path
from langchain_chroma import Chroma
from luna_chatbot.app.rag.document_loader import chunked_documents
from luna_chatbot.app.models.embedding import basic_embedding
import os
from dotenv import load_dotenv

load_dotenv()


def get_persist_dir() -> Path:
    """
    Bevorzugt absoluten Pfad aus ENV (LUNA_DATA_DIR).
    Fallback: <CWD>/data/chroma_vectorstorage (im Container ist CWD = /app).
    Legt den Ordner an.
    """
    env_path = os.getenv("LUNA_DATA_DIR")
    base = (
        Path(env_path) if env_path else (Path.cwd() / "data" / "chroma_vectorstorage")
    )
    base = base.resolve()
    base.mkdir(parents=True, exist_ok=True)
    return base


PERSIST_DIR = get_persist_dir()

vector_storage = Chroma(
    collection_name="RAG_Collection",
    embedding_function=basic_embedding,
    persist_directory=PERSIST_DIR,
)


def main():
    """Main function to set vector store."""
    ids = vector_storage.add_documents(documents=chunked_documents)

    if ids:
        return

    raise Exception("Could not set VectorStore")


if __name__ == "__main__":
    main()
