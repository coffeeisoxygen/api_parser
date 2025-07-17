"""repository layer for modules.yaml, berbasis file yaml.
Desain modular agar mudah migrasi ke database nantinya.
"""

from pathlib import Path

import yaml

from src.config.base_settings import settings
from src.schemas.sch_module import ModuleItem, ProductItem

# Default path for module YAML file
DEFAULT_PATH = settings.module_yaml_path


class ModuleRepoYaml:
    def __init__(self, file_path: Path = DEFAULT_PATH):
        self.file_path = Path(file_path)
        self._modules = self._load_modules()

    def _load_modules(self) -> list[ModuleItem]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r") as f:
            data = yaml.safe_load(f) or {}

        raw_modules = data.get("modules", [])
        return [ModuleItem(**item) for item in raw_modules]

    def all(self) -> list[ModuleItem]:
        return self._modules.copy()

    def get_by_code(self, code: str) -> ModuleItem | None:
        return next((m for m in self._modules if m.code == code), None)

    def find_product_by_code(
        self, product_code: str
    ) -> tuple[ModuleItem, ProductItem] | None:
        for module in self._modules:
            for product in module.products:
                if product.code == product_code:
                    return module, product
        return None
