from guard.decorators import SecurityDecorator
from guard.models import SecurityConfig

from src.config.app_config import settings


def str_to_bool(val: str) -> bool:
    """Konversi string ke boolean."""
    return str(val).lower() in ("true", "1", "yes")


def str_to_list(val: str) -> list:
    """Konversi string dipisah koma ke list."""
    return [x.strip() for x in val.split(",") if x.strip()]


config = SecurityConfig(
    whitelist=str_to_list(settings.whitelist),
    blacklist=str_to_list(settings.blacklist),
    blocked_user_agents=str_to_list(settings.blocked_user_agents),
    auto_ban_threshold=settings.auto_ban_threshold,
    auto_ban_duration=settings.auto_ban_duration,
    custom_log_file=settings.custom_log_file,
    rate_limit=settings.rate_limit,
    enforce_https=settings.enforce_https,
    enable_cors=settings.enable_cors,
    cors_allow_origins=str_to_list(settings.cors_allow_origins),
    cors_allow_methods=str_to_list(settings.cors_allow_methods),
    cors_allow_headers=str_to_list(settings.cors_allow_headers),
    cors_allow_credentials=settings.cors_allow_credentials,
    cors_expose_headers=str_to_list(settings.cors_expose_headers),
    cors_max_age=settings.cors_max_age,
    block_cloud_providers=set(str_to_list(settings.block_cloud_providers)),
)

guard_deco = SecurityDecorator(config)
