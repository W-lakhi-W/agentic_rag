from uuid import uuid4
import shutil

from fastapi import Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from auth.db import get_db
from auth.security import get_current_user
from rag.models import Document
from auth.models import User
from rag.config import UPLOAD_DIR



async def upload_pdfs(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    uploaded_documents = []

    for file in files:

        # Validate PDF
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{file.filename} is not a PDF."
            )

        # Generate unique filename
        unique_filename = f"{uuid4()}.pdf"

        file_path = UPLOAD_DIR / unique_filename

        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get file size
        file_size = file_path.stat().st_size

        # Save metadata
        document = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_path=str(file_path),
            status="PENDING",
        )

        db.add(document)
        db.flush()  # Generates document.id without committing

        uploaded_documents.append(
            {
                "document_id": document.id,
                "filename": document.filename,
                "file_path": document.file_path
            }
        )

    db.commit()

    return {
        "message": "Files uploaded successfully.",
        "documents": uploaded_documents,
    }