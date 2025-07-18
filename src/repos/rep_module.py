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

    def __init__(self, file_path: Path = default_path) -> None:
        super().__init__(file_path)

    def get_by_moduleid(self, moduleid: str) -> Module | None:
        """Get a module by its unique module ID.

        This method retrieves a module from the repository using its module ID.

        Args:
            moduleid (str): moduleid yang ingin diambil
                Contoh: "M001"

        Returns:
            Module | None: Module yang ditemukan atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return next(
            (m for m in self._items if getattr(m, "moduleid", None) == moduleid), None
        )

    def get_all_module_listip(self) -> list[str] | None:
        """Get a list of unique IP addresses from modules.

        This method retrieves all unique IP addresses from the modules in the repository.

        Returns:
            list[str] | None: Daftar IP yang ditemukan atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return (
            list({m.base_url for m in self._items if getattr(m, "base_url", None)})
            or None
        )

    def get_all_active_only_module(self) -> list[Module] | None:
        """Get all active modules only.

        This method retrieves all modules from the repository that are currently active.

        Returns:
            list[Module] | None: Daftar modul yang aktif atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return [m for m in self._items if getattr(m, "is_active", False)] or None

    def get_list_module(self) -> list[Module]:
        """Get a list of all modules.

        This method retrieves all modules from the repository.

        Returns:
            list[Module]: Daftar semua modul.
        """
        return list(self._items)

    def get_list_active_only(self) -> list[Module]:
        """Get a list of active modules only.

        This method retrieves all active modules from the repository.

        Returns:
            list[Module]: Daftar modul yang aktif.
        """
        return [m for m in self._items if getattr(m, "is_active", False)]

    def get_by_moduleip(self, ip: str) -> Module | None:
        """Get a module by its IP address.

        This method retrieves a module from the repository using its IP address.

        Args:
            ip (str): Alamat IP yang ingin diambil

        Returns:
            Module | None: Module yang ditemukan atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return next(
            (m for m in self._items if getattr(m, "base_url", None) == ip), None
        )

    def get_list_moduleip(self) -> list[str]:
        """Get a list of unique IP addresses from modules.

        This method retrieves all unique IP addresses from the modules in the repository.

        Returns:
            list[str]: Daftar IP yang ditemukan.
        """
        return list({m.base_url for m in self._items if getattr(m, "base_url", None)})
