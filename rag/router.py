from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from rag import controller
from auth.security import get_current_user, get_db
from auth.models import User
from rag.schemas import SendMessageRequest


rag_routes = APIRouter(prefix="/api")

@rag_routes.post("/ingest")
async def ingest_pdf(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
   return await controller.ingest_pdf(files, db, current_user)


@rag_routes.post("/chat")
async def new_chat(
    title: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.new_chat(title, db, current_user)

@rag_routes.post("/chat/{chat_id}")
async def send_message(
    chat_id: int,
    body: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.send_message(chat_id, body.message, db, current_user)

@rag_routes.get("/chat/{chat_id}")
async def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.get_chat(chat_id, db, current_user)

@rag_routes.get("/chats")
async def get_all_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.get_all_chats(db, current_user)

@rag_routes.delete("/chat/{chat_id}")
async def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.delete_chat(chat_id, db, current_user)

@rag_routes.get("/documents")
async def get_all_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.get_all_documents(db, current_user)

@rag_routes.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.delete_document(document_id, db, current_user)

@rag_routes.get("/documents/{document_id}")
async def view_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await controller.view_document(document_id, db, current_user)