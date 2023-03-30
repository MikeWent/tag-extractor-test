import subprocess
from os import getenv

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(getenv("DATABASE_URL"))
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
)


async def dispose_db():
    await engine.dispose()


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with async_session() as session:
        await session.execute(select(1))
    # perform migrations
    subprocess.run(["python3", "-m", "alembic", "upgrade", "head"])
