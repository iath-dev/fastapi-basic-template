from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_setting
from app.core.deps import get_database
from app.schemas.base import ResponseBase

router = APIRouter(tags=["System"])


_settings = get_setting()


@router.get("/", response_model=ResponseBase)
async def root():
    """Root endpoint"""
    return ResponseBase(
        data={
            "message": "Welcome to FastAPI Portfolio Backend",
            "version": _settings.VERSION,
            "environment": _settings.ENVIRONMENT,
            "docs": "/docs",
            "api": _settings.API_V1_STR,
        }
    )


@router.get("/health", response_model=ResponseBase)
async def health_check(db: Annotated[AsyncSession, Depends(get_database)]):
    """Health check endpoint"""
    db_status = "disconnected"
    db_error = None

    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        db_status = "connected"
    except Exception as e:
        db_error = str(e)

    return ResponseBase(
        success=db_status == "connected",
        message="healthy"
        if db_status == "connected"
        else "unhealthy - database disconnected",
        data={
            "status": "healthy" if db_status == "connected" else "unhealthy",
            "environment": _settings.ENVIRONMENT,
            "version": _settings.VERSION,
            "api_version": _settings.API_V1_STR,
            "database": db_status,
            "database_error": db_error if db_error else None,
        },
    )


@router.get("/info", response_model=ResponseBase)
async def app_info(db: Annotated[AsyncSession, Depends(get_database)]):
    """Application information endpoint"""
    db_info = {"status": "disconnected", "version": None}

    try:
        # Get PostgreSQL version
        result = await db.execute(text("SELECT version();"))
        version = result.fetchone()
        db_info["status"] = "connected"
        db_info["version"] = version[0].split(",")[0] if version else None
    except Exception as e:
        db_info["error"] = str(e)

    return ResponseBase(
        data={
            "name": _settings.PROJECT_NAME,
            "version": _settings.VERSION,
            "environment": _settings.ENVIRONMENT,
            "api_version": _settings.API_V1_STR,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "database": db_info,
        }
    )
