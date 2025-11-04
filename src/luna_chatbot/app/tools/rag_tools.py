from langchain.tools import tool
from luna_chatbot.app.rag.vector_store import vector_storage


@tool()
async def get_RAG_data(query: str) -> str:
    """
    use whenever receiving a question about a nursing care related question.

    returns a list of data chunks

    args:
      question str

    returns:
    str

    """
    # TODO: refactor with fully built rag_agent

    result = await vector_storage.asearch(query=query, search_type="mmr", k=10)

    if len(result) != 0:
        readable_result = f"Das habe ich zur frage '{query}' gefunden:\n\n"

        for r in result:
            print(r.metadata)
            readable_result += f"**PDF:** {r.metadata['source']}\n **Page:** {r.metadata['page_label']} \n **Content:** \n{r.page_content}\n\n"

        return readable_result

    else:
        return ""
