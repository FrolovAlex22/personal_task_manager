# import time

# from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.core.config import settings
from app.db.models import Base
# from core.models.files_model import Files
# from core.models.users_model import Users

engine = create_async_engine(
    settings.DATABASE_URL,
    # "sqlite+aiosqlite:///fastapi.db",
    echo=True,
    future=True,
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def create_model():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)