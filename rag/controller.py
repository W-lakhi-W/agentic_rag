from sqlalchemy.orm import Session
from fastapi import UploadFile
from auth.models import User
from rag.models import Chat
from rag.Ingesting.upload_pdf import upload_pdfs
from rag.Ingesting.loader import load_pdf
from rag.Ingesting.splitter import split_documents
from rag.vectordb import vector_db
from rag.query.create_chat import create_chat
from rag.query.save_message import save_message
from rag.query.retrive_chat_history import get_chat_history
from rag.llm import model
from rag.prompt import prompt



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

    vector_db.add_documents(all_chunks)
    return {"message": "PDFs ingested and stored successfully."}
    

async def query_pdf(
    query: str,
    db: Session,
    current_user: User,
):
    results = vector_db.similarity_search(query, k=20)
    
    return {"message": f"Query received: {query}", "results": results}

async def new_chat(
    title: str,
    db: Session,
    current_user: User,
):
    new_chat = create_chat(db, current_user.id, title)
    save_message(db, new_chat.id, "user", content=new_chat.title)
    chat_history = get_chat_history(db, new_chat.id)
    prompt_message = prompt.invoke({"question": title, "chat_history": chat_history})
    model_response = model.invoke(prompt_message)
    save_message(db, new_chat.id, "assistant", content=model_response.content)

    return {"message": model_response}

async def send_message(
    chat_id: int,
    message: str,
    db: Session,
    current_user: User,
):
    save_message(db, chat_id, "user", content=message)
    chat_history = get_chat_history(db, chat_id)
    prompt_message = prompt.invoke({"question": message, "chat_history": chat_history})
    model_response = model.invoke(prompt_message)
    save_message(db, chat_id, "assistant", content=model_response.content)

    return {"message": model_response}

async def get_chat(
    chat_id: int,
    db: Session,
    current_user: User,
):
    chat_history = get_chat_history(db, chat_id, current_user.id)
    return {"chat_history": chat_history}

async def get_all_chats(
    db: Session,
    current_user: User,
):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).all()
    return {"chats": chats}

async def delete_chat(
    chat_id: int,
    db: Session,
    current_user: User,
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        return {"error": "Chat not found or you do not have permission to delete it."}
    
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully."}