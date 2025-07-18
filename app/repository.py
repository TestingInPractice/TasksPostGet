from sqlalchemy import select
from app.models import Task
from app.schemas import TaskCreate, Task as TaskRead, TaskStatus  # TaskRead — схема ответа (Pydantic)
from app.database import async_session  # или new_session
from datetime import datetime


class TaskRepository:
    @classmethod
    async def add_task(cls, task_data: TaskCreate, created_by: str = "system_user") -> TaskRead:
        async with async_session() as session:
            new_task = Task(
                name=task_data.name,
                description=task_data.description,
                status=TaskStatus.created,
                created_at=datetime.utcnow(),
                created_by=created_by,
                updated_at=None,
                updated_by=None,
            )
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            # Преобразуем ORM-модель (Task) в Pydantic-схему (TaskRead)
            return TaskRead.model_validate(new_task)

    @classmethod
    async def get_all_tasks(cls) -> list[TaskRead]:
        async with async_session() as session:
            result = await session.execute(select(Task))
            tasks = result.scalars().all()
            # Преобразуем все задачи в список Pydantic-схем
            return [TaskRead.model_validate(task) for task in tasks]
