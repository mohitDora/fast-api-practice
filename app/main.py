from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import todo
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router, prefix="/api", tags=["todos"])