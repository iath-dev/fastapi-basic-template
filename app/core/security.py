from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_setting

settings = get_setting()


_SECRET_KEY = settings.SECRET_KEY
_ALGORITHM = settings.ALGORITHM
_ACCESS_TOKEN_EXPIRES_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
_REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


class SecurityManager:
    """Security Manager"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.ALGORITHM = _ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = _ACCESS_TOKEN_EXPIRES_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = _REFRESH_TOKEN_EXPIRE_DAYS

    def hash_password(self, password: str) -> str:
        """Generate hashed password

        Args:
            password (str): Password

        Returns:
            str: Hashed password
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify the hashed password

        Args:
            plain_password (str): Plain password
            hashed_password (str): Hashed password to compare

        Returns:
            bool: It valid or not he password
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str:
        """Create an access token for a user.

        Args:
            user (User): The user object.
            expires_delta (Optional[timedelta]): The expiration time delta. Defaults to ACCESS_TOKEN_EXPIRES_MINUTES.

        Returns:
            str: The encoded access token.
        """
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=_ACCESS_TOKEN_EXPIRES_MINUTES)
        )
        to_encode = {"sub": str(subject), "exp": expire}
        return jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)

    def create_refresh_token(self, subject: str | Any) -> str:
        """Method to create the refresh token

        Args:
            subject (Union[str, Any]): Data to encode in the token

        Returns:
            str: Refresh token
        """
        return self.create_access_token(
            subject=subject, expires_delta=timedelta(self.REFRESH_TOKEN_EXPIRE_DAYS)
        )

    def decode_token(self, token: str, options: dict | None = None) -> dict | None:
        """Decode the token

        Args:
            token (str): Token
            options (Optional[dict], optional): Token decode options. Defaults to None.

        Returns:
            Optional[dict]: Token decoded data
        """
        try:
            return jwt.decode(
                token, _SECRET_KEY, algorithms=[_ALGORITHM], options=options
            )
        except JWTError:
            return None

    def get_token_data(self, token: str, ignore_expiration: bool = False) -> dict:
        """Get the token payload data

        Args:
            token (str): Token string
            ignore_expiration (bool, optional): Ignore if the token is already expired. Defaults to False.

        Returns:
            dict: Token payload
        """
        options = {"verify_exp": not ignore_expiration}
        payload = self.decode_token(token, options=options)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload


security_manager = SecurityManager()
