from sqlalchemy.orm import Session
from rag.models import Message,Chat

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)


def get_chat_history(
    db: Session,
    chat_id: int,
    user_id: int,
) -> list[Message]:
    """
    Retrieve all messages for a chat ordered by creation time.
    """

    # history = (
    #     db.query(Message)
    #     .filter(Message.chat_id == chat_id)
    #     .order_by(Message.created_at.asc())
    #     .all()
    # )
    history = (
        db.query(Message)
        .join(Chat, Message.chat_id == Chat.id)
        .filter(
            Chat.id == chat_id,
            Chat.user_id == user_id,
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    conversation = [
        (
            HumanMessage(content=msg.content)
            if msg.role.lower() == "user"
            else AIMessage(content=msg.content)
            if msg.role.lower() == "assistant"
            else SystemMessage(content=msg.content)
        )
        for msg in history
    ]
    return conversation

def get_chat_messages(
    db: Session,
    chat_id: int,
    user_id: int,
):
    return (
        db.query(Message)
        .join(Chat, Message.chat_id == Chat.id)
        .filter(
            Chat.id == chat_id,
            Chat.user_id == user_id,
        )
        .order_by(Message.created_at.asc())
        .all()
    )