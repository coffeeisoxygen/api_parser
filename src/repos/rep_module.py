"""repository layer for modules.yaml, berbasis file yaml.

Desain modular agar mudah migrasi ke database nantinya.

Made by Hasan Maki and ChatGPT
"""

from pathlib import Path

from src.config.base_settings import settings
from src.repos.base_repo import BaseYamlRepo
from src.schemas.sch_base_modules import Module

# Default path for module YAML file
default_path = settings.module_yaml_path


class ModuleRepoYaml(BaseYamlRepo[Module]):
    yaml_key = "modules"
    model = Module
    unique_key_fn = staticmethod(lambda x: x["moduleid"])
    unique_name = "module id"

    def __init__(self, file_path: Path = default_path):
        super().__init__(file_path)

    def get_by_moduleid(self, moduleid: str) -> Module | None:
        """Ambil module berdasarkan moduleid."""
        return next((m for m in self._items if m.moduleid == moduleid), None)

    def get_listip(self) -> list[str]:
        """Get list of unique base_url from modules."""
        return list({m.base_url for m in self._items if m.base_url})
