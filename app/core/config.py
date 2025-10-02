from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalSettings(BaseSettings):
    """
    Application settings loaded from environment variables
    Users .env file in development, actual env vars in production.
    """

    # Basic app config
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Portfolio Backend"
    VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str
    SYNC_DATABASE_URL: str | None = None

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Convert postgres:// to postgresql+asyncpg:// if needed"""
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("SYNC_DATABASE_URL")
    @classmethod
    def validate_sync_database_url(cls, v: str, values) -> str:
        """Convert postgresql+asyncpg:// to postgresql:// if needed"""
        if v:
            return v
        db_url = values.data.get("DATABASE_URL")
        if db_url.startswith("postgresql+asyncpg://"):
            return db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
        return db_url

    # CORS origins
    BACKEND_CORS_ORIGINS: list[str] | None = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and v:
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        return []

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )


@lru_cache
def get_setting():
    """Get the setting of the project"""
    return GlobalSettings()
