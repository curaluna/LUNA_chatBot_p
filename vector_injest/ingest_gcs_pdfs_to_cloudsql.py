import os
import asyncio
import tempfile
from pathlib import Path
import uuid
from google.cloud import storage
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from langchain_postgres import PGEngine, PGVectorStore

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def list_pdf_blobs(bucket_name: str, prefix: str = "") -> list[str]:
    """Listet PDF-Objekte in einem Bucket (optional Prefix)."""
    client = storage.Client()
    blobs = client.list_blobs(bucket_name, prefix=prefix)  # official pattern
    return [b.name for b in blobs if b.name.lower().endswith(".pdf")]


def download_blob_to_file(bucket_name: str, blob_name: str, target_path: Path) -> None:
    """Lädt ein GCS-Objekt in eine lokale Datei."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(str(target_path))


async def main():
    # --- Config ---
    bucket = os.environ["GCS_BUCKET"]
    prefix = os.getenv("GCS_PREFIX", "")

    pg_user = os.environ["POSTGRES_USER"]
    pg_pass = os.environ["POSTGRES_PASSWORD"]
    pg_db = os.environ["POSTGRES_DB"]
    table = os.getenv("VECTOR_TABLE", "agent_vectors")

    # Cloud SQL Proxy -> localhost
    conn_str = f"postgresql+psycopg://{pg_user}:{pg_pass}@127.0.0.1:5432/{pg_db}"

    # --- List PDFs in GCS ---
    pdf_blobs = list_pdf_blobs(bucket, prefix)
    if not pdf_blobs:
        print(f"Keine PDFs gefunden in gs://{bucket}/{prefix}")
        return

    # --- Embeddings (Dimension automatisch bestimmen) ---
    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBED_MODEL", "text-embedding-3-large")
    )
    dim = len(embeddings.embed_query("dimension probe"))

    # Async SQLAlchemy engine (psycopg3)
    async_engine = create_async_engine(conn_str, pool_pre_ping=True)
    pg_engine = PGEngine.from_engine(engine=async_engine)

    # Immer frisch: Tabelle droppen + neu anlegen
    schema = "public"
    async with async_engine.begin() as conn:
        await conn.execute(text(f'DROP TABLE IF EXISTS "{schema}"."{table}" CASCADE;'))
        # optional, aber praktisch:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    await pg_engine.ainit_vectorstore_table(table_name=table, vector_size=dim)

    store = await PGVectorStore.create(
        engine=pg_engine,
        table_name=table,
        embedding_service=embeddings,
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

    # --- Download -> Parse -> Chunk -> Upsert ---
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        total_chunks = 0
        for blob_name in pdf_blobs:
            local_pdf = tmpdir / Path(blob_name).name
            download_blob_to_file(bucket, blob_name, local_pdf)

            # PyPDFLoader liest Seiten + Metadaten
            loader = PyPDFLoader(str(local_pdf))
            pages = loader.load()  # pro Seite ein Document
            # Wichtig: Quelle stabil halten (GCS-Pfad)
            for d in pages:
                d.metadata["source"] = f"gs://{bucket}/{blob_name}"

            chunks = splitter.split_documents(pages)

            # Optional: stabile IDs (hilft bei Dedupe-Strategien)
            for i, c in enumerate(chunks):
                src = c.metadata.get("source", "")
                page = c.metadata.get("page", "na")
                stable_key = f"{src}#p{page}-c{i}"
                c.id = str(uuid.uuid5(uuid.NAMESPACE_URL, stable_key))

            await store.aadd_documents(chunks)
            total_chunks += len(chunks)
            print(f"{blob_name}: {len(chunks)} chunks")

        print(f"Fertig. Insgesamt {total_chunks} chunks in '{table}' gespeichert.")


if __name__ == "__main__":
    asyncio.run(main())
