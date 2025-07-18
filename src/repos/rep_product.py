"""repository layer for products.yaml, berbasis file yaml.

Desain modular agar mudah migrasi ke database nantinya.
"""

from pathlib import Path

import yaml

from src.config.base_settings import settings
from src.repos.rep_helper import validate_unique
from src.schemas.sch_base_products import Product
from src.utils.mylogger import logger

# Default path for product YAML file
DEFAULT_PATH = settings.product_yaml_path


class ProductRepoYaml:
    def __init__(self, file_path: Path = DEFAULT_PATH):
        self.file_path = Path(file_path)
        self._products = self._load_products()

    def _load_products(self) -> list[Product]:
        if not self.file_path.exists():
            logger.warning(f"Product file not found: {self.file_path}")
            return []

        with self.file_path.open("r") as f:
            data = yaml.safe_load(f) or {}

        raw_products = data.get("products", [])
        try:
            validate_unique(raw_products, lambda x: x["code"], name="product code")
        except Exception as e:
            logger.error(f"Failed to load products: {e}")
            raise
        logger.info(f"Loaded {len(raw_products)} products from {self.file_path}")
        return [Product(**item) for item in raw_products]

    def all(self) -> list[Product]:
        return self._products.copy()

    def get_by_code(self, code: str) -> Product | None:
        return next((p for p in self._products if p.code == code), None)

    def get_listprovider(self) -> list[str]:
        """Get list of unique providers from products."""
        return list({p.provider for p in self._products if p.provider})
