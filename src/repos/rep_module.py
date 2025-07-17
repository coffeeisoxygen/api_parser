"""repository layer for modules.yaml, berbasis file yaml.
Desain modular agar mudah migrasi ke database nantinya.

Made by Hasan Maki and ChatGPT
"""

from pathlib import Path

import yaml

from src.config.base_settings import settings
from src.schemas.sch_module import Module, Product

# Default path for module YAML file
DEFAULT_PATH = settings.module_yaml_path


class ModuleRepoYaml:
    def __init__(self, file_path: Path = DEFAULT_PATH):
        self.file_path = Path(file_path)
        self._modules = self._load_modules()

    def _load_modules(self) -> list[Module]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r") as f:
            data = yaml.safe_load(f) or {}

        raw_modules = data.get("modules", [])
        return [Module(**item) for item in raw_modules]

    def all(self) -> list[Module]:
        """Ambil semua module beserta products-nya."""
        return self._modules.copy()

    def get_by_code(self, code: str) -> Module | None:
        """Ambil module berdasarkan kode."""
        return next((m for m in self._modules if m.code == code), None)

    def find_product_by_code(self, product_code: str) -> tuple[Module, Product] | None:
        """Cari product berdasarkan kode, dan kembalikan module + product-nya."""
        for module in self._modules:
            for product in module.products:
                if product.code == product_code:
                    return module, product
        return None

    def get_product_only(self, product_code: str) -> Product | None:
        """Ambil hanya object Product berdasarkan kode."""
        found = self.find_product_by_code(product_code)
        return found[1] if found else None
