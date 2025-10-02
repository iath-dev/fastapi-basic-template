from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository with specific business logic (async)
    """

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email"""
        result = await self.db.execute(
            select(self.model).filter(self.model.email == email)
        )

        return result.scalar_one_or_none()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all active users"""
        result = await self.db.execute(
            select(self.model).filter(self.model.is_active).offset(skip).limit(limit)
        )

        return list(result.scalars().all())
