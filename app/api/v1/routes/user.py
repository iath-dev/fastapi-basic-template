from fastapi import APIRouter, Depends

from app.schemas.base import PaginationMeta, PaginationResponse, ResponseBase
from app.schemas.user import UserCreate, UserInDB
from app.services.user_service import UserService, get_user_service

router = APIRouter(tags=["Users"])

_user_service = Depends(get_user_service)


@router.get("/", response_model=PaginationResponse[UserInDB])
async def get_users(
    user_service: UserService = _user_service,
    skip: int = 0,
    limit: int = 100,
):
    """Get all users"""
    total, users = await user_service.list_users(skip, limit)

    meta = PaginationMeta(
        page=(skip // limit) + 1,
        per_page=limit,
        total=total,
        pages=(total + limit - 1) // limit,
        has_next=skip + limit < total,
        has_prev=skip > 0,
    )

    return PaginationResponse(data=users, meta=meta)


@router.post("/", response_model=ResponseBase[UserInDB])
async def create_user(
    user: UserCreate,
    user_service: UserService = _user_service,
):
    """Create and user"""
    user = await user_service.create_user(email=user.email, password=user.password)

    return ResponseBase.success_response(data=user)
