# Modules ini untuk Load settings dari file env / setup default app.

from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings

from src.exceptions.system_exceptions import RegistryFileNotFoundError
from src.utils.mylogger import logger


class AppConfiguration(BaseSettings):
    app_host: str = Field(default="127.0.0.1", description="Host aplikasi")
    app_port: int = Field(default=8000, description="Port aplikasi")
    app_log_level: str = Field(default="info", description="Level log aplikasi")
    app_mode: str = Field(default="development", description="Mode aplikasi")

    # Registry files (YAML)
    member_yaml_path: Path = Field(
        default=Path("registry/members.yaml"), description="Path file member registry"
    )
    module_yaml_path: Path = Field(
        default=Path("registry/modules.yaml"), description="Path file module registry"
    )
    product_yaml_path: Path = Field(
        default=Path("registry/products.yaml"), description="Path file produk registry"
    )
    mapping_yaml_path: Path = Field(
        default=Path("registry/mappings.yaml"), description="Path file mapping registry"
    )

    # Security config
    whitelist: str = Field(
        default="127.0.0.1,::1,192.168.1.1,2001:db8::1",
        description="IP whitelist, comma separated",
    )
    blacklist: str = Field(
        default="10.0.0.1,2001:db8::2", description="IP blacklist, comma separated"
    )
    blocked_user_agents: str = Field(
        default="curl,wget", description="Blocked user agents, comma separated"
    )
    auto_ban_threshold: int = Field(default=5, description="Auto ban threshold")
    auto_ban_duration: int = Field(
        default=86400, description="Auto ban duration in seconds"
    )
    custom_log_file: str = Field(
        default="security.log", description="Custom log file for security"
    )
    rate_limit: int = Field(default=100, description="Rate limit")
    enforce_https: bool = Field(default=False, description="Enforce HTTPS")
    enable_cors: bool = Field(default=True, description="Enable CORS")
    cors_allow_origins: str = Field(
        default="*", description="CORS allow origins, comma separated"
    )
    cors_allow_methods: str = Field(
        default="GET,POST", description="CORS allow methods, comma separated"
    )
    cors_allow_headers: str = Field(
        default="*", description="CORS allow headers, comma separated"
    )
    cors_allow_credentials: bool = Field(
        default=True, description="CORS allow credentials"
    )
    cors_expose_headers: str = Field(
        default="X-Custom-Header", description="CORS expose headers, comma separated"
    )
    cors_max_age: int = Field(default=600, description="CORS max age")
    block_cloud_providers: str = Field(
        default="AWS,GCP,Azure", description="Blocked cloud providers, comma separated"
    )

    # model config
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def model_post_init(self, __context: Any) -> None:
        self._validate_paths_exist()

    def _validate_paths_exist(self):
        paths = {
            "member_yaml_path": self.member_yaml_path,
            "module_yaml_path": self.module_yaml_path,
            "product_yaml_path": self.product_yaml_path,
            "mapping_yaml_path": self.mapping_yaml_path,
        }
        for name, path in paths.items():
            if not path.exists():
                logger.error(f"[Startup] File {name} tidak ditemukan: {path}")
                raise RegistryFileNotFoundError(name, str(path))


settings = AppConfiguration()
