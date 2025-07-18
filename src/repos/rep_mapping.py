"""repository layer for mappings.yaml, berbasis file yaml.

Desain modular agar mudah migrasi ke database nantinya.
"""

from pathlib import Path

from src.config.base_settings import settings
from src.repos.base_repo import BaseYamlRepo
from src.schemas.sch_base_mappings import ProductModuleMapping

# Default path for mappings YAML file
DEFAULT_PATH = settings.mapping_yaml_path


class MappingRepoYaml(BaseYamlRepo[ProductModuleMapping]):
    yaml_key = "product_module_mapping"
    model = ProductModuleMapping
    unique_key_fn = staticmethod(lambda x: (x["product_code"], x["module_code"]))
    unique_name = "product_code+module_code combination"

    def __init__(self, file_path: Path = DEFAULT_PATH):
        super().__init__(file_path)

    def get_by_product_and_module(
        self, product_code: str, module_code: str
    ) -> ProductModuleMapping | None:
        return next(
            (
                m
                for m in self._items
                if m.product_code == product_code and m.module_code == module_code
            ),
            None,
        )

    def get_active(self) -> list[ProductModuleMapping]:
        return [m for m in self._items if m.is_active]

    def get_by_product(self, product_code: str) -> list[ProductModuleMapping]:
        return [m for m in self._items if m.product_code == product_code]

    def get_by_module(self, module_code: str) -> list[ProductModuleMapping]:
        return [m for m in self._items if m.module_code == module_code]

    def get_list_active_only(self) -> list[ProductModuleMapping]:
        return [m for m in self._items if getattr(m, "is_active", False)]

    def get_list_mapping(self) -> list[ProductModuleMapping]:
        return list(self._items)
