from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

def store_documents(
    chunks: list[Document],
    embedding_model: HuggingFaceEmbeddings,
    collection_name: str = "documents",
    persist_directory: str = "./chroma_db",

):
    vector_db = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory,
    )

    vector_db.add_documents(chunks)

    return vector_db