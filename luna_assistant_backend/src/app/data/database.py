import os
from contextlib import asynccontextmanager

from google.cloud.sql.connector import Connector, IPTypes
from psycopg import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.engine import URL

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION")
INSTANCE_NAME = os.getenv("CLOUD_SQL_INSTANCE_NAME")

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

USE_CLOUDSQL_CONNECTOR = os.getenv("USE_CLOUDSQL_CONNECTOR", "false").lower() == "true"

VECTOR_TABLE = "agent_vectors"


def getconn_asyncpg():
    """Create a Cloud SQL connection using the Python Connector and asyncpg.

    This function is only used when USE_CLOUDSQL_CONNECTOR is enabled.
    The returned connection is managed and closed by SQLAlchemy via the
    engine's creator callback.
    """
    if not (PROJECT_ID and REGION and INSTANCE_NAME):
        raise RuntimeError(
            "Cloud SQL Connector requires GCP_PROJECT_ID, GCP_REGION "
            "and CLOUD_SQL_INSTANCE_NAME to be set."
        )

    instance = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"

    connector = Connector()
    conn = connector.connect(
        instance,
        "asyncpg",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        ip_type=IPTypes.PUBLIC,
        enable_iam_auth=False,
    )
    return conn


def get_engine() -> AsyncEngine:
    """Create an AsyncEngine for accessing the pgvector-enabled Postgres database.

    The engine is primarily used by the vector store. By default, it connects
    directly via DB_HOST and DB_PORT using asyncpg. If USE_CLOUDSQL_CONNECTOR
    is set to true, the Google Cloud SQL Python Connector is used instead.

    Returns:
        AsyncEngine: SQLAlchemy async engine configured for Postgres.

    Raises:
        RuntimeError: If no valid database configuration can be derived
            from the environment variables.
    """
    if DB_HOST and not USE_CLOUDSQL_CONNECTOR:
        db_url = URL.create(
            "postgresql+asyncpg",
            username=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        return create_async_engine(db_url, pool_pre_ping=True)

    if USE_CLOUDSQL_CONNECTOR:
        if not (PROJECT_ID and REGION and INSTANCE_NAME):
            raise RuntimeError(
                "USE_CLOUDSQL_CONNECTOR=true, but GCP_PROJECT_ID, GCP_REGION "
                "or CLOUD_SQL_INSTANCE_NAME are missing."
            )
        return create_async_engine(
            "postgresql+asyncpg://",
            creator=getconn_asyncpg,
        )

    raise RuntimeError(
        "No valid database configuration found. Provide DB_HOST/DB_PORT or "
        "enable USE_CLOUDSQL_CONNECTOR with the required GCP_* variables."
    )


@asynccontextmanager
async def get_checkpointer_conn():
    """Yield an AsyncConnection for use with the LangGraph AsyncPostgresSaver.

    The connection uses the same database configuration as the vector store.
    Autocommit is enabled to simplify checkpoint writes. The connection is
    automatically closed when the context manager exits.

    Yields:
        AsyncConnection: An open psycopg AsyncConnection instance.

    Raises:
        RuntimeError: If neither a direct host/port configuration nor a valid
            Cloud SQL configuration is available.
    """
    conn_kwargs = {
        "user": DB_USER,
        "password": DB_PASS,
        "dbname": DB_NAME,
    }

    if DB_HOST and not USE_CLOUDSQL_CONNECTOR:
        conn_kwargs.update({"host": DB_HOST, "port": DB_PORT})
    elif USE_CLOUDSQL_CONNECTOR and PROJECT_ID and REGION and INSTANCE_NAME:
        conn_kwargs["host"] = f"/cloudsql/{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
    else:
        raise RuntimeError(
            "Missing DB configuration: provide DB_HOST/DB_PORT or enable "
            "USE_CLOUDSQL_CONNECTOR with GCP_PROJECT_ID, GCP_REGION and "
            "CLOUD_SQL_INSTANCE_NAME."
        )

    conn = await AsyncConnection.connect(**conn_kwargs)
    await conn.set_autocommit(True)

    try:
        yield conn
    finally:
        await conn.close()
