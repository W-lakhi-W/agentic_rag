from sqlalchemy.orm import Session
from rag.models import Chat

def create_chat(db: Session, user_id: int, title: str = None):
    chat = Chat(user_id=user_id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat