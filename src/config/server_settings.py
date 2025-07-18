"""settings for server configuration."""

from src.config.app_config import settings
from src.utils.mylogger import LogContext, logger


def get_uvicorn_config():
    """Return Uvicorn config dict from AppSettings."""
    config = {
        "host": settings.app_host,
        "port": settings.app_port,
        "log_level": "INFO",
        "reload": settings.app_mode == "development",
    }
    with LogContext("Load Uvicorn config", level="INFO"):
        logger.info(f"Uvicorn configuration loaded: {config}")
    return config
