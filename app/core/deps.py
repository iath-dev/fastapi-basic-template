from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


# Database dependency
async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """Database dependency"""
    async for db in get_db():
        yield db


# Type alias for cleaner code
DatabaseDep = Depends(get_database)
