from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppError


async def app_exception_handler(request: Request, exc: AppError):
    """Handle all custom application exceptions.
    Returns standardized error response

    Args:
        request (Request): Request
        exc (AppError): App error

    Returns:
        JSONResponse: App response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "detail": exc.detail,
            "path": str(request.url),
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation error from request body/query params.
    Transforms into readable format

    Args:
        request (Request): API Request
        exc (RequestValidationError): Pydantic error

    Returns:
        JSONResponse: JSON Response
    """
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"][1:]),
                "message": error["msg"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "message": "Validation error",
            "errors": errors,
            "path": str(request.url),
        },
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handle database integrity errors (unique constraints, foreign keys, etc).
    Avoid exposing internal DB structure.

    Args:
        request (Request): API Request
        exc (IntegrityError): Error

    Returns:
        JSONResponse: APP Response
    """
    detail = None
    if exc.orig and hasattr(exc.orig, "args"):
        detail = str(exc.orig.args[0]) if exc.orig.args else None

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "message": "Database constraint violation",
            "detail": detail,
            "path": str(request.url),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unhandled exceptions.
    Log full error but return safe message to client

    Args:
        request (Request): API Request
        exc (Exception): Exception

    Returns:
        JSONResponse: JSON Response
    """
    logger.exception(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error", "path": str(request.url)},
    )
