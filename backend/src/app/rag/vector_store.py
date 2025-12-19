from pathlib import Path
from langchain_chroma import Chroma
from app.rag.document_loader import get_chunked_documents
from app.models.embedding import basic_embedding
import os


def get_persist_dir() -> Path:
    """
    Bevorzugt absoluten Pfad aus ENV (LUNA_DATA_DIR).
    Fallback: <CWD>/data/chroma_vectorstorage (im Container ist CWD = /app).
    Legt den Ordner an.
    """
    env_path = os.getenv("LUNA_DATA_DIR")
    base = Path(env_path) if env_path else (Path.cwd() / "data" / "chroma_vectorstorage")
    base = base.resolve()
    base.mkdir(parents=True, exist_ok=True)
    return base


PERSIST_DIR = get_persist_dir()

vector_storage = Chroma(
    collection_name="RAG_Collection",
    embedding_function=basic_embedding,
    persist_directory=PERSIST_DIR,
)


def clear_vector_storage() -> None:
    """Delete all stored vectors to ensure a clean re-index."""
    existing_ids = vector_storage.get().get("ids", [])
    if existing_ids:
        vector_storage.delete(ids=existing_ids)
    existing_ids = vector_storage.get().get("ids", [])
    if len(existing_ids) == 0:
        print("\033[32mvector-store deleted successfully\033[0m", end="\n\n")

    else:
        raise Exception("There was an Error with the vector-store deletion.")


def main():
    """Main function to set vector store."""
    clear_vector_storage()
    ids = vector_storage.add_documents(documents=get_chunked_documents())

    if ids:
        return

    raise Exception("Could not set VectorStore")


if __name__ == "__main__":
    main()
