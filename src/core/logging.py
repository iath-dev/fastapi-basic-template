import sys
from pathlib import Path

from loguru import logger

from src.core.config import get_setting

_settings = get_setting()


def setup_logging():
    """Configure loguru logger bases on environment"""

    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=_settings.LOG_LEVEL,
        colorize=True,
    )

    if _settings.ENVIRONMENT == "production":
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)

        # Error logs
        logger.add(
            log_path / "error.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )

        # All logs (with rotation)
        logger.add(
            log_path / "app.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
            rotation="50 MB",
            retention="7 days",
            compression="zip",
        )

    # Development: detailed file logging
    elif _settings.ENVIRONMENT == "development":
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)

        logger.add(
            log_path / "dev.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="3 days",
        )

    # Intercept standard logging (for SQLAlchemy, uvicorn, etc.)
    import logging

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:  # type: ignore
                frame = frame.f_back  # type: ignore
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Replace handlers for standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Adjust log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if _settings.ENVIRONMENT == "development" else logging.WARNING
    )

    logger.info(f"Logging configured for {_settings.ENVIRONMENT} environment")

    return logger
