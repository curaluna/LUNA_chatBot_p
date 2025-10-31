from pathlib import Path
from langchain_chroma import Chroma
from luna_chatbot.app.rag_builder import chunked_documents
from luna_chatbot.app.models import basic_embedding

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
    """Mai""n function to set vector store."""
    print("Attempting to set VectorStore")
    ids = vector_storage.aadd_documents(documents=chunked_documents)

    if ids:
        print("Successfully set VectorStore")
        return
    raise Exception("Could not set VectorStore")


if __name__ == "__main__":
    main()
