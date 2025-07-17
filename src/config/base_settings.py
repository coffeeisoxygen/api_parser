# Modules ini untuk Load settings dari file env / setup default app.

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
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

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = AppSettings()
