from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from rag import controller
from auth.security import get_current_user, get_db
from auth.models import User


rag_routes = APIRouter(prefix="/api")

@rag_routes.post("/ingest")
async def ingest_pdf(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

   return await controller.ingest_pdf(files, db, current_user)