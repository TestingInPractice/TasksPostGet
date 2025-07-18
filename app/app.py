# app/app.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_tables
from .tasks_router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home():
    return {"data": "Code -v мешке"}

app.include_router(tasks_router)
