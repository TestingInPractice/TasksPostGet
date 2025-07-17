from datetime import datetime                       # Импорт класса для работы с датой и временем
from typing import Optional                         # Импорт типа для необязательных (Optional) полей
from pydantic import BaseModel, Field               # Импорт базовой модели и функции Field для описания полей
from pydantic.config import ConfigDict              # Импорт класса для настройки конфигурации модели
from enum import Enum                               # Импорт для создания Enum статусов



# Описываем перечень допустимых статусов задачи в виде Enum с англоязычными кодами
class TaskStatus(str, Enum):
    created = "created"
    active = "active"
    closed = "closed"

class TaskCreate(BaseModel):                         # Модель данных для создания задачи
    name: str = Field(..., description="Название задачи")           # Обязательное поле: название задачи с описанием
    description: Optional[str] = Field(None, description="Описание задачи")  # Необязательное поле: описание задачи с описанием

class Task(TaskCreate):
    id: int = Field(..., description="Уникальный идентификатор задачи")
    created_at: datetime = Field(..., description="Дата и время создания задачи")
    created_by: str = Field(..., description="Пользователь, создавший задачу")
    updated_at: Optional[datetime] = Field(None, description="Дата и время последнего изменения задачи")
    updated_by: Optional[str] = Field(None, description="Пользователь, который последним изменил задачу")
    status: TaskStatus = Field(..., description="Статус задачи")

    model_config = ConfigDict(from_attributes=True)  # Настройка модели, позволяющая создавать объекты из атрибутов (например, ORM объекты)
