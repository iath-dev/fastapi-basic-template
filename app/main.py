from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.exc import IntegrityError

from app.api.router import api_router
from app.core.config import get_setting
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.exceptions.handlers import (
    app_exception_handler,
    generic_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)

_settings = get_setting()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("🚀 Starting FastAPI application")
    logger.info(f"Environment: {_settings.ENVIRONMENT}")
    logger.info(f"Version: {_settings.VERSION}")
    logger.debug(f"Database URL: {_settings.DATABASE_URL[:50]}...")
    await create_db_and_tables()
    yield
    logger.info("⛔ Shutting down FastAPI application")


def create_application() -> FastAPI:
    """
    Application factory pattern
    Creates and configures FastAPI instance
    """
    app = FastAPI(
        title=_settings.PROJECT_NAME,
        version=_settings.VERSION,
        openapi_url=f"{_settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    app.add_exception_handler(AppError, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    if _settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=_settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router)

    return app


app = create_application()
