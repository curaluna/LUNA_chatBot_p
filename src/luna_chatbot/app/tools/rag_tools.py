from langchain.tools import tool
from luna_chatbot.app.rag_builder.vector_store import vector_storage


@tool(description="Retrekives informations from the german 'Pflegeratgeber des BMG'")
async def get_care_info(query: str) -> list[str]:
    """
    use when answering topics related to nursing care, healthcare  or general care

    args:
      question str

    returns:
    list[str]

    """
    # TODO: refactor with fully built rag_agent
    result = await vector_storage.asearch(query=query, search_type="mmr", k=3)
    if len(result) != 0:
        print(result)
        readable_result = f"Das habe ich zur frage '{query}' gefunden:\n\n"

        for r in result:
            readable_result += f"PDF: {r.metadata['source']}\n Page: {r.metadata['page_label']} \n Content: \n{r.page_content}\n\n"

        return readable_result

    else:
        return ""
