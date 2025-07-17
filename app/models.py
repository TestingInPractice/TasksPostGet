from datetime import datetime                       # Импорт для работы с датой и временем
from typing import Optional
import enum                                        # Импорт для создания перечисления (Enum)
from .database import Base

from sqlalchemy import (
    Column,                                       # Для описания колонок таблицы
    Integer,                                      # Тип колонки: целое число
    String,                                       # Тип колонки: строка
    DateTime,                                     # Тип колонки: дата и время
    Enum as SqlEnum,                              # Тип колонки для enum в базе данных
)
from sqlalchemy.orm import declarative_base       # Базовый класс для ORM-моделей


class TaskStatus(enum.Enum):                        # Перечисление со статусами задачи
    created = "created"                            # Статус "создана"
    active = "active"                              # Статус "активна"
    closed = "closed"                              # Статус "закрыта"

class Task(Base):                                  # Модель задачи, наследуется от Base
    __tablename__ = "tasks"                        # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)   # Первичный ключ, индексируемый
    name = Column(String, nullable=False)                 # Название задачи (обязательно)
    description = Column(String, nullable=True)           # Описание задачи (необязательно)
    status = Column(SqlEnum(TaskStatus), nullable=False, default=TaskStatus.created)  # Статус задачи с дефолтом
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)            # Дата и время создания, по умолчанию текущее время
    created_by = Column(String, nullable=False)              # Кто создал задачу (например, username)
    updated_at = Column(DateTime, nullable=True)             # Дата и время последнего обновления, не обязательно
    updated_by = Column(String, nullable=True)               # Кто последний изменил задачу (необязательно)
