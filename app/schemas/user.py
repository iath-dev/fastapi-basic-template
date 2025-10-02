from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema, TimestampMixin, UUIDMixin


class UserBase(BaseSchema):
    """Base schema for user"""

    email: EmailStr = Field("base@example.com", description="User email")


class UserCreate(UserBase):
    """Schema for user creation"""

    password: str = Field(..., description="User password")


class UserUpdate(UserBase):
    """Schema for user update"""

    password: str | None = None


class UserInDB(UserBase, UUIDMixin, TimestampMixin):
    """Schema for user in database"""

    is_active: bool = Field(..., description="User is active")


class UserSchema(UserBase, UUIDMixin, TimestampMixin):
    """Schema for user"""

    is_active: bool = Field(..., description="User is active")
