"""setup loguru for logging with advanced configuration."""

from venv import logger

from src.config.app_config import AppConfiguration
from src.utils.mylogger import LogConfig, patch_uvicorn_loggers, setup_logging

# Load settings from the AppSettings
settings = AppConfiguration()
# Configure logging using settings
log_config = LogConfig(
    level=settings.app_log_level.upper(),
    to_terminal=True,
    name_prefix=settings.app_mode,
)


def initialize_logging():
    """Initialize logging configuration."""
    setup_logging(log_config)
    logger.info("Logging initialized with level: %s", settings.app_log_level)
    patch_uvicorn_loggers()
    logger.info("Uvicorn loggers patched for advanced logging.")
