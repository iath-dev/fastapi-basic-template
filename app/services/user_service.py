from fastapi import Depends

from app.core.exceptions import AuthenticationError
from app.core.security import security_manager
from app.models.user import User
from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.user import CreateUser


class UserService:
    """
    Business logic layer (async)
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, email: str, password: str) -> User:
        """Create a new user with validation"""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Hash password (simplified for example)
        hashed_password = security_manager.hash_password(password)

        user_data = CreateUser(email=email, hashed_password=hashed_password)

        return await self.user_repository.create(user_data)

    async def get_user(self, user_id: int) -> User | None:
        """Get user by ID"""
        return await self.user_repository.get_by_id(user_id)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List all users"""
        return await self.user_repository.get_all(skip, limit)

    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user"""
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise AuthenticationError()

        valid = security_manager.verify_password(password, user.hashed_password)

        if not valid:
            raise AuthenticationError()

        return user

    async def update_user(self, user_id: int, **kwargs) -> User | None:
        """Update user data"""
        return await self.user_repository.update(user_id, kwargs)

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        return await self.user_repository.delete(user_id)


_user_repository = Depends(get_user_repository)


async def get_user_service(
    user_repository: UserRepository = _user_repository,
) -> UserService:
    return UserService(user_repository)
