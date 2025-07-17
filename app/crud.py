from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Task
from app.schemas import TaskCreate, TaskStatus
from datetime import datetime

async def create_task(
    session: AsyncSession,
    task_create: TaskCreate,
    created_by: str,
) -> Task:
    new_task = Task(
        name=task_create.name,
        description=task_create.description,
        status=TaskStatus.created,      # Статус задаётся сервером как "created"
        created_at=datetime.utcnow(),
        created_by=created_by,
        updated_at=None,
        updated_by=None,
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)  # Обновляем объект, чтобы получить id и др. поля
    return new_task

async def get_all_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return tasks
