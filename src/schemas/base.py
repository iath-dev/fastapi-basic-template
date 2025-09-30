from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configurations"""

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for object with timestamps"""

    created_at: datetime
    updated_at: datetime


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key"""

    id: UUID


class ResponseBase(BaseSchema, Generic[T]):
    """Base response schema"""

    success: bool = True
    message: str = "Operation successful"
    data: T | None = None


class PaginationMeta(BaseSchema):
    """Pagination metadata"""

    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


class PaginationResponse(ResponseBase[list[T]]):
    """Paginated response schema"""

    meta: PaginationMeta


class ErrorDetail(BaseSchema):
    """Error detail schema"""

    field: str | None = None
    message: str
    code: str | None = None


class ErrorResponse(BaseSchema):
    """Error response schema"""

    success: bool = False
    message: str
    errors: list[ErrorDetail] | None = None
    data: Any | None = None
