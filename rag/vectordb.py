from langchain_chroma import Chroma
from rag.Ingesting.embedding import embedding_model

vector_db = Chroma(
        collection_name="documents",
        embedding_function=embedding_model,
        persist_directory="./chroma_db",
    )
