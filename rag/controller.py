from sqlalchemy.orm import Session
from fastapi import UploadFile
from auth.models import User
from rag.Ingesting.upload_pdf import upload_pdfs
from rag.Ingesting.loader import load_pdf
from rag.Ingesting.splitter import split_documents
from rag.Ingesting.embedding import embedding_model
from rag.vectordb import store_documents



async def ingest_pdf(
    files: list[UploadFile],
    db: Session,
    current_user: User,
):
    documents = await upload_pdfs(files, db, current_user)

    all_chunks = []

    for document in documents["documents"]:
        file_path = document["file_path"]
        documents_content = load_pdf(file_path)
        chunks = split_documents(documents_content)

        for chunk in chunks:
            chunk.metadata.update({
                "user_id": current_user.id,
                "document_id": document["document_id"],
                "filename": document["filename"],
            })
        all_chunks.extend(chunks)

    store_documents(chunks=all_chunks, embedding_model=embedding_model)
    return {"message": "PDFs ingested and stored successfully."}
    

