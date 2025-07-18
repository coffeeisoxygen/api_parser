from guard import SecurityConfig, SecurityDecorator, SecurityMiddleware


def get_security_config() -> SecurityConfig:
    # Bisa tambahkan logika dinamis di sini jika perlu
    return SecurityConfig(
        whitelist=["192.168.1.1", "2001:db8::1"],
        blacklist=["10.0.0.1", "2001:db8::2"],
        blocked_user_agents=["curl", "wget"],
        auto_ban_threshold=5,
        auto_ban_duration=86400,
        custom_log_file="security.log",
        rate_limit=100,
        enforce_https=True,
        enable_cors=True,
        cors_allow_origins=["*"],
        cors_allow_methods=["GET", "POST"],
        cors_allow_headers=["*"],
        cors_allow_credentials=True,
        cors_expose_headers=["X-Custom-Header"],
        cors_max_age=600,
        block_cloud_providers={"AWS", "GCP", "Azure"},
    )


def get_guard_decorator(config: SecurityConfig) -> SecurityDecorator:
    return SecurityDecorator(config)


def get_guard_middleware(config: SecurityConfig) -> tuple:
    """Return tuple (middleware_class, config) untuk add_middleware."""
    return (SecurityMiddleware, {"config": config})
