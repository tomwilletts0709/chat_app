import os
from datetime import timedelta, datetime, timezone
from typing import Annotated, Optional

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from chat_app.chat_schema import Token, TokenData, User, AuthUser, AuthUserResponse
from chat_app.db import get_db
from chat_app.models import User as UserModel
from chat_app.repository import get_user_by_username
from pwdlib import PasswordHash
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash()


def verify_password(plain_password: Optional[str], hashed_password: Optional[str]) -> bool:
    if not plain_password or not hashed_password:
        return False
    return password_hash.verify(hashed_password, plain_password)


def get_password_hash(password: Optional[str]) -> str:
    if not password:
        return ""
    return password_hash.hash(password)


def authenticate_user(db: Session, username: Optional[str], password: Optional[str]) -> Optional[UserModel]:
    user = get_user_by_username(db, username) if username else None
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    username = payload.get("sub")
    return TokenData(username=username)


def get_current_user(
    token_data: TokenData = Depends(verify_token),
    db: Session = Depends(get_db),
):
    if not token_data.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user = get_user_by_username(db, token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def get_current_active_user(
    current_user = Depends(get_current_user),
):
    # Could add disabled check when User model has disabled field
    return current_user
