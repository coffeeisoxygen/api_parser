from guard.models import SecurityConfig
from guard import SecurityDecorator, SecurityMiddleware
from src.config.app_config import settings


def get_security_config() -> SecurityConfig:
    # Bisa tambahkan logika dinamis di sini jika perlu
    return SecurityConfig()


def get_guard_decorator(config: SecurityConfig) -> SecurityDecorator:
    return SecurityDecorator(config)


def get_guard_middleware(config: SecurityConfig) -> tuple:
    """Return tuple (middleware_class, config) untuk add_middleware."""
    return (SecurityMiddleware, {"config": config})
