from fastapi import APIRouter

from app.api.v1.routes import user

api_v1_router = APIRouter()

api_v1_router.include_router(user.router, prefix="/users", tags=["Users"])
