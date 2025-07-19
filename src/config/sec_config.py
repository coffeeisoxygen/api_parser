import os

from dotenv import load_dotenv
from guard.decorators import SecurityDecorator
from guard.models import SecurityConfig

# Load environment variables from security.env
load_dotenv(os.path.join(os.path.dirname(__file__), "../../security.env"))


def str_to_bool(val):
    return str(val).lower() in ("true", "1", "yes")


def str_to_list(val):
    return [x.strip() for x in val.split(",") if x.strip()]


config = SecurityConfig(
    whitelist=str_to_list(os.getenv("WHITELIST", "")),
    blacklist=str_to_list(os.getenv("BLACKLIST", "")),
    blocked_user_agents=str_to_list(os.getenv("BLOCKED_USER_AGENTS", "")),
    auto_ban_threshold=int(os.getenv("AUTO_BAN_THRESHOLD", 5)),
    auto_ban_duration=int(os.getenv("AUTO_BAN_DURATION", 86400)),
    custom_log_file=os.getenv("CUSTOM_LOG_FILE", "security.log"),
    rate_limit=int(os.getenv("RATE_LIMIT", 100)),
    enforce_https=str_to_bool(os.getenv("ENFORCE_HTTPS", True)),
    enable_cors=str_to_bool(os.getenv("ENABLE_CORS", True)),
    cors_allow_origins=str_to_list(os.getenv("CORS_ALLOW_ORIGINS", "*")),
    cors_allow_methods=str_to_list(os.getenv("CORS_ALLOW_METHODS", "GET,POST")),
    cors_allow_headers=str_to_list(os.getenv("CORS_ALLOW_HEADERS", "*")),
    cors_allow_credentials=str_to_bool(os.getenv("CORS_ALLOW_CREDENTIALS", True)),
    cors_expose_headers=str_to_list(
        os.getenv("CORS_EXPOSE_HEADERS", "X-Custom-Header")
    ),
    cors_max_age=int(os.getenv("CORS_MAX_AGE", 600)),
    block_cloud_providers=set(
        str_to_list(os.getenv("BLOCK_CLOUD_PROVIDERS", "AWS,GCP,Azure"))
    ),
)

guard_deco = SecurityDecorator(config)
