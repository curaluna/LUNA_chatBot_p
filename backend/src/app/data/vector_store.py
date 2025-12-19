from langchain_postgres import PGEngine, PGVectorStore
from app.data.database import get_engine, VECTOR_TABLE


async def get_vectorstore(embeddings):
    sa_engine = get_engine()
    pg_engine = PGEngine.from_engine(sa_engine)

    # WICHTIG: keine Table-Init Calls!
    store = await PGVectorStore.create(
        engine=pg_engine,
        table_name=VECTOR_TABLE,
        embedding_service=embeddings,
    )
    return store
