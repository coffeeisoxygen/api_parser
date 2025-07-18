"""repository layer for products.yaml, berbasis file yaml.

Desain modular agar mudah migrasi ke database nantinya.
"""

from pathlib import Path

from src.config.base_settings import settings
from src.repos.base_repo import BaseYamlRepo
from src.schemas.sch_base_products import Product

# Default path for product YAML file
default_path = settings.product_yaml_path


class ProductRepoYaml(BaseYamlRepo[Product]):
    yaml_key = "products"
    model = Product
    unique_key_fn = staticmethod(lambda x: x["code"])
    unique_name = "product code"

    def __init__(self, file_path: Path = default_path):
        super().__init__(file_path)

    def get_by_code(self, code: str) -> Product | None:
        return next((p for p in self._items if p.code == code), None)

    def get_listprovider(self) -> list[str]:
        """Get list of unique providers from products."""
        return list({p.provider for p in self._items if p.provider})
