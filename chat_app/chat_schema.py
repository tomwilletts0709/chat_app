from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    chat_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageRead]] = None

    class Config:
        from_attributes = True


# Auth-related schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str


class AuthUser(BaseModel):
    username: str
    email: str
    password: str


class AuthUserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
