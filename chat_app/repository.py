from typing import List, Optional
from sqlalchemy.orm import Session

from chat_app.models import Chat, Message, User
from chat_app.chat_schema import ChatCreate, MessageCreate


def get_chats(db: Session) -> List[Chat]:
    return db.query(Chat).all()


def get_chat(db: Session, chat_id: int) -> Optional[Chat]:
    return db.query(Chat).filter(Chat.id == chat_id).first()


def create_chat(db: Session, chat: ChatCreate) -> Chat:
    db_chat = Chat(title=chat.title)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def create_message(db: Session, message: MessageCreate, chat_id: int) -> Message:
    db_message = Message(content=message.content, chat_id=chat_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(db: Session, chat_id: int) -> List[Message]:
    return db.query(Message).filter(Message.chat_id == chat_id).all()


def get_message(db: Session, message_id: int) -> Optional[Message]:
    return db.query(Message).filter(Message.id == message_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()
