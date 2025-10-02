from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Business logic layer (async)
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, email: str, username: str, password: str) -> User:
        """Create a new user with validation"""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        existing_username = await self.user_repository.get_by_username(username)
        if existing_username:
            raise ValueError("Username already taken")

        # Hash password (simplified for example)
        hashed_password = f"hashed_{password}"

        user_data = {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "is_active": True,
        }

        return await self.user_repository.create(user_data)

    async def get_user(self, user_id: int) -> User | None:
        """Get user by ID"""
        return await self.user_repository.get_by_id(user_id)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List all users"""
        return await self.user_repository.get_all(skip, limit)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate a user"""
        user = await self.user_repository.get_by_email(email)
        if user and user.hashed_password == f"hashed_{password}":
            return user
        return None

    async def update_user(self, user_id: int, **kwargs) -> User | None:
        """Update user data"""
        return await self.user_repository.update(user_id, kwargs)

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        return await self.user_repository.delete(user_id)
