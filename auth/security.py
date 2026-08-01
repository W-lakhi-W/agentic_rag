from auth.db import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from auth.models import User
import jwt
from datetime import datetime, timedelta, timezone
from auth.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)



def get_user(db: Session, username: str) -> User | None:
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    user = get_user(db, username)

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire , "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id_int = int(user_id)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id_int).first()
    if user is None:
        raise credentials_exception
    return user
