from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.settings import get_settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(get_settings().db_url, echo=True)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI - yields a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()  # Commit on successful completion
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_db_session_context() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for notebooks/scripts - use with 'async with'."""
    async for session in get_db_session():
        yield session
        break


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
