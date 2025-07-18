# Modules ini untuk Load settings dari file env / setup default app.

from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class RegistryFileNotFoundError(FileNotFoundError):
    def __init__(self, name: str, path: Path) -> None:
        super().__init__(f"[Startup Error] File '{name}' tidak ditemukan: {path}")


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
    product_yaml_path: Path = Field(
        default=Path("registry/products.yaml"), description="Path file produk registry"
    )
    mapping_yaml_path: Path = Field(
        default=Path("registry/mappings.yaml"), description="Path file mapping registry"
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
                raise RegistryFileNotFoundError(name, path)


settings = AppSettings()
