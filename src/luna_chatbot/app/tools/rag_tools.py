from langchain.tools import tool
from luna_chatbot.app.rag.vector_store import vector_storage


@tool()
async def get_RAG_data(query: str) -> list[str]:
    """
    Use to fetch up-to-date, nursing-, health-, or caregiving-related knowledge from the vector store; pass along the user’s full query and weave the retrieved highlights into your reply.

    args:
      question str

    returns:
    list[str]

    """
    # TODO: refactor with fully built rag_agent

    result = await vector_storage.asearch(query=query, search_type="mmr", k=5)
    if len(result) != 0:
        print(result)
        readable_result = f"Das habe ich zur frage '{query}' gefunden:\n\n"

        for r in result:
            readable_result += f"PDF: {r.metadata['source']}\n Page: {r.metadata['page_label']} \n Content: \n{r.page_content}\n\n"

        return readable_result

    else:
        return ""
