from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TaskCreate, Task as TaskRead
from .database import async_session, create_tables
from .models import Task  # IMPORT моделей, чтобы они были зарегистрированы в Base!
from .crud import create_task, get_all_tasks
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте приложения создаём таблицы
    await create_tables()
    yield
    # при выключении приложения здесь можно освободить ресурсы, если нужно

app = FastAPI(lifespan=lifespan)

# Зависимость: получение асинхронной сессии из фабрики async_session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.get("/")
async def home():
    return {"data": "Code -v мешке"}

@app.post("/tasks/", response_model=TaskRead)
async def add_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session),
    # сюда можно добавить current_user или подобное, чтобы передать created_by
):
    # Для демонстрации передаём статическое имя создателя
    created_by = "system_user"

    db_task = await create_task(session, task, created_by=created_by)
    return db_task

@app.get("/tasks/", response_model=list[TaskRead])
async def read_tasks(session: AsyncSession = Depends(get_session)):
    tasks = await get_all_tasks(session)
    return tasks
