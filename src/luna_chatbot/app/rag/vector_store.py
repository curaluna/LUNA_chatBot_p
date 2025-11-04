from pathlib import Path
from langchain_chroma import Chroma
from luna_chatbot.app.rag.document_loader import chunked_documents
from luna_chatbot.app.models.embedding import basic_embedding
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_DIR = Path(__file__).resolve().parents[4] / "data" / "chroma_vectorstorage"

vector_storage = Chroma(
    collection_name="RAG_Collection",
    embedding_function=basic_embedding,
    persist_directory=DATABASE_DIR,
)


def main():
    """Main function to set vector store."""
    ids = vector_storage.add_documents(documents=chunked_documents)

    if ids:
        return

    raise Exception("Could not set VectorStore")


if __name__ == "__main__":
    main()
