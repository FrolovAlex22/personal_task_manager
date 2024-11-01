# import time

import contextlib
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.core.config import settings
from app.db.models import Base
# from core.models.files_model import Files
# from core.models.users_model import Users

# engine = create_async_engine(
#     settings.DATABASE_URL,
#     # "sqlite+aiosqlite:///fastapi.db",
#     echo=True,
#     future=True,
# )
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )
class DatabaseSessionManager:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager не инициализирован")
        await self.engine.dispose()

        self.engine = None
        self.session_factory = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("DatabaseSessionManager не инициализирован")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.session_factory is None:
            raise Exception("DatabaseSessionManager не инициализирован")

        session = self.session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(url=settings.DB.URL, echo=False)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

async def create_models():
    async with sessionmanager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_models():
    async with sessionmanager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
