from langchain.tools import tool
from langgraph.prebuilt import ToolRuntime

from rag.vectordb import vector_db


@tool
def retrieve_chunks(query: str, runtime: ToolRuntime) -> list[dict]:
    """
    Retrieve relevant document chunks from the current user's uploaded documents.

    Searches the user's vector store for content relevant to the query.
    Returns only information from the user's documents. If no relevant
    content is found, an empty result is returned so the agent can
    decide how to respond.
    """
    current_user_id = runtime.context["user_id"]
    results = vector_db.similarity_search(
        query,
        k=5,
        filter={"user_id": current_user_id},
    )
    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
        }
        for document in results
    ]
