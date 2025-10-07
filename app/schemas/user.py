from pydantic import ConfigDict, EmailStr, Field

from app.schemas.base import BaseSchema, TimestampMixin, UUIDMixin


class UserBase(BaseSchema):
    """Base schema for user"""

    email: EmailStr = Field("base@example.com", description="User email")


class UserCreate(UserBase):
    """Schema for user creation"""

    password: str = Field("2HYcRiDeN", description="User password")


class UserUpdate(UserCreate):
    """Schema for user update"""

    pass


class CreateUser(UserBase):
    """Schema for user creation"""

    hashed_password: str = Field(..., description="User password")

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase, UUIDMixin, TimestampMixin):
    """Schema for user in database"""

    is_active: bool = Field(..., description="User is active")


class UserSchema(UserBase, UUIDMixin, TimestampMixin):
    """Schema for user"""

    is_active: bool = Field(..., description="User is active")
