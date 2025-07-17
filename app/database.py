# подключение к базе и управление сессиями
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"   # Путь к базе SQLite (можно адаптировать)

# Создаём асинхронный движок базы данных
engine = create_async_engine(
    DATABASE_URL,
    echo=True,                    # Вывод SQL-запросов в консоль (можно отключить)
    future=True,
)

# Фабрика асинхронных сессий — объект для создания сессий работы с БД
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession                    # оставлено по умолчанию
)

# Абстрактный базовый класс для моделей ORM
class Base(DeclarativeBase):
    pass

# Функции для создания и удаления таблиц (использовать при старте/выключении приложения)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
