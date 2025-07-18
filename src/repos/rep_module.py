"""repository layer for modules.yaml, berbasis file yaml.

Desain modular agar mudah migrasi ke database nantinya.

Made by Hasan Maki and ChatGPT
"""

from pathlib import Path

import yaml

from src.config.base_settings import settings
from src.repos.rep_helper import validate_unique
from src.schemas.sch_base_modules import Module
from src.utils.mylogger import logger

# Default path for module YAML file
DEFAULT_PATH = settings.module_yaml_path


class ModuleRepoYaml:
    def __init__(self, file_path: Path = DEFAULT_PATH):
        self.file_path = Path(file_path)
        self._modules = self._load_modules()

    def _load_modules(self) -> list[Module]:
        if not self.file_path.exists():
            logger.warning(f"Module file not found: {self.file_path}")
            return []

        with self.file_path.open("r") as f:
            data = yaml.safe_load(f) or {}

        raw_modules = data.get("modules", [])
        try:
            validate_unique(raw_modules, lambda x: x["code"], name="module code")
        except Exception as e:
            logger.error(f"Failed to load modules: {e}")
            raise
        logger.info(f"Loaded {len(raw_modules)} modules from {self.file_path}")
        return [Module(**item) for item in raw_modules]

    def all(self) -> list[Module]:
        """Ambil semua module."""
        return self._modules.copy()

    def get_by_code(self, code: str) -> Module | None:
        """Ambil module berdasarkan kode."""
        return next((m for m in self._modules if m.code == code), None)

    def get_listip(self) -> list[str]:
        """Get list of unique IPs from modules."""
        return list({m.base_url for m in self._modules if m.base_url})
