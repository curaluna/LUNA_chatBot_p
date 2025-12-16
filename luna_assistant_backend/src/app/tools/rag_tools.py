from langchain_core.tools import tool
from app.data.vector_store import get_vectorstore
from app.models.embedding import basic_embedding


@tool
async def get_RAG_data(query: str) -> str:
    """
    Search the knowledge base for relevant documents based on the user query.
    Useful for answering questions about specific documents, policies, or technical details stored in the database.
    """

    try:
        vector_store = await get_vectorstore(basic_embedding)

        results = await vector_store.asimilarity_search(query, k=5)

        if not results:
            return "No relevant information found in the knowledge base."

        formatted_docs = "\n\n---\n\n".join(
            [
                f"Content: {doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}"
                for doc in results
            ]
        )

        return formatted_docs

    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"
