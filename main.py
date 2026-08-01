from fastapi import FastAPI
from auth.router import auth_routes
from rag.router import rag_routes
from auth.db import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth_routes)
app.include_router(rag_routes)