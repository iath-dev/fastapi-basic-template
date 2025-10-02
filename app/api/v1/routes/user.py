from fastapi import APIRouter, Depends

from app.core.deps import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.base import ResponseBase
from app.schemas.user import UserCreate, UserSchema

router = APIRouter(tags=["Users"])

_get_user_repository: UserRepository = Depends(get_user_repository)


@router.get("/", response_model=ResponseBase[list[UserSchema]])
async def get_users(
    user_repository=_get_user_repository,
    skip: int = 0,
    limit: int = 100,
):
    """Get all users"""
    users = await user_repository.get_all(skip, limit)
    return ResponseBase(data=users)


@router.post("/", response_model=ResponseBase[UserSchema])
async def create_user(
    user: UserCreate,
    user_repository=_get_user_repository,
):
    """Create and user"""
    print(user)
