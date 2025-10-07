import uuid
from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.schemas.base import BaseModel

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with common CRUD operations
    """

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: uuid.UUID) -> ModelType | None:
        """Get a single record by ID"""
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[ModelType]]:
        """Get all records with pagination"""
        count_query = select(func.count()).select_from(self.model)
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        items = list(result.scalars().all())

        return total, items

    async def create(self, obj_in: BaseModel) -> ModelType:
        """Create a new record"""

        obj_data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def update(self, id: uuid.UUID, obj_in: BaseModel | dict) -> ModelType | None:
        """Update an existing record"""
        db_obj = await self.get_by_id(id)

        if not db_obj:
            return None

        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.model_dump(exclude_unset=True)
        )

        for key, value in update_data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: uuid.UUID) -> bool:
        """Delete a record by ID"""
        db_obj = await self.get_by_id(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True

        return False
