from fastapi import APIRouter, Depends
from auth import controller
from auth.schemas import UserCreate,LoginRequest
from sqlalchemy.orm import Session
from auth.db import get_db
from auth.security import get_current_user
from auth.models import User


auth_routes = APIRouter(prefix="/auth")

@auth_routes.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db) ):
    return controller.register_user(user,db)

@auth_routes.post("/login")
async def login_user(user: LoginRequest, db: Session = Depends(get_db)):
    return controller.login_user(user, db)


@auth_routes.get("/get_user")
async def get_user(current_user: User = Depends(get_current_user)):
    return controller.get_user(current_user)
