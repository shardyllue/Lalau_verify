from utils.config import PG_URL

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncEngine,
    async_sessionmaker, AsyncSession
)



engine = create_async_engine(
    url="postgresql+asyncpg://" + PG_URL,
    pool_size=20, max_overflow=0,
    pool_recycle=True
)
engine_posting = create_async_engine(
    url="postgresql+asyncpg://" + PG_URL,
    pool_size=20, max_overflow=0,
    pool_recycle=True
)

Session = async_sessionmaker(bind=engine, expire_on_commit=True)
SessionPosting = async_sessionmaker(bind=engine_posting, expire_on_commit=True)
