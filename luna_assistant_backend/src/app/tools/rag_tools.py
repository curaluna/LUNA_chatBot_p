from langchain.tools import tool
from app.rag.vector_store import vector_storage


@tool("dataFetch")
async def get_RAG_data(query: str) -> str:
    """
    Search the internal knowledge base built from PDF brochures about:
    - nursing care and care settings (home care, nursing homes, support services)
    - care levels, benefits, costs, and related regulations
    - specific conditions (e.g. arthrosis, dementia, heart failure, IBD)
    - assistive technology and safety (emergency call systems, GPS trackers,
      smart home / assisted living solutions)

    Use this tool when:
    - the user asks for concrete factual information, definitions, options,
      comparisons or step-by-step guidance related to these topics, or
    - you need reliable details (numbers, conditions, requirements, pros/cons)
      that are likely documented in the PDFs.

    Do NOT use this tool for:
    - general chit-chat, opinions, or emotional support
    - programming, math, or topics clearly unrelated to care, health,
      benefits, or assistive technology.

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
            readable_result += f"**PDF:** {r.metadata['title']}\n **Page:** {r.metadata['page_label']} \n **Content:** \n{r.page_content}\n\n"

        return readable_result

    else:
        return ""
