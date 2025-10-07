from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """User database model"""

    __tablename__ = "users"

    email: Mapped[String] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[String] = mapped_column(String, nullable=False)
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True)
