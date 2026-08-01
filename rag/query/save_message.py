
from sqlalchemy.orm import Session
from rag.models import Message

def save_message(
    db: Session,
    chat_id: int,
    role: str,
    content: str,
):
    message = Message(
        chat_id=chat_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message