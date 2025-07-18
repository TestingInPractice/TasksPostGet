# app/tasks_router.py

from fastapi import APIRouter
from app.schemas import TaskCreate, Task as TaskRead
from app.repository import TaskRepository  # путь зависит от структуры файлов

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)

@router.post("/", response_model=TaskRead)
async def add_task(task: TaskCreate):
    # created_by — можно сделать через Depends, если потом нужен login
    return await TaskRepository.add_task(task, created_by="system_user")

@router.get("/", response_model=list[TaskRead])
async def get_tasks():
    return await TaskRepository.get_all_tasks()
