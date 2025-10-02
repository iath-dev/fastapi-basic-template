from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository


# Database dependency
async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """Database dependency"""
    async for db in get_db():
        yield db


_get_database = Depends(get_database)


async def get_user_repository(
    db: AsyncSession = _get_database,
) -> UserRepository:
    """
    User repository dependency injection (async)
    """
    return UserRepository(db)


# Type alias for cleaner code
DatabaseDep = Depends(get_database)
