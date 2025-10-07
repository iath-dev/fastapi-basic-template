from typing import Any


class AppError(Exception):
    """Base exception for all application errors"""

    def __init__(self, message, status_code: int = 500, detail: Any = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class EntityNotFoundError(AppError):
    """Raised when a database entity is not found"""

    def __init__(self, entity: str, identifier: Any):
        super().__init__(
            message=f"{entity} not found",
            status_code=404,
            detail={"entity": entity, "identifier": str(identifier)},
        )


class ValidationError(AppError):
    """Raised when business validation fails"""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(
            message, status_code=422, detail={"field": field} if field else None
        )


class AuthenticationError(AppError):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401, detail=None)


class AuthorizationError(AppError):
    """Raised when user lacks permissions"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403, detail=None)


class DuplicateEntityError(AppError):
    """Raised when trying to create a duplicate entity"""

    def __init__(self, entity: str, field: str, value: Any):
        super().__init__(
            message=f"{entity} with {field}='{value}' already exists",
            status_code=409,
            detail={"entity": entity, "field": field, "value": str(value)},
        )
