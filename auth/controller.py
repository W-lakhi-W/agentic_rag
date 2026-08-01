from auth.schemas import UserCreate, LoginRequest
from sqlalchemy.orm import Session
from auth.models import User
from auth.security import hash_password, verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException, status

def register_user(user: UserCreate, db: Session):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def login_user(user: LoginRequest, db: Session):
    # Find the user by username
    db_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Generate tokens
    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "role": db_user.role,
        }
    )

    # Store refresh token (preferably store its hash)
    refresh_token = create_refresh_token(
        data={
            "sub": str(db_user.id),
            "role": db_user.role,
        }
    )
    db_user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

def get_user(current_user: User):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }

