from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar

import aiofiles
import yaml

from src.exceptions.app_exceptions import AppException
from src.repos.base_validator import validate_unique
from src.utils.mylogger import logger

T = TypeVar("T")


class BaseYamlRepo(Generic[T]):
    # --- konfigurasi default (override di subclass) ---
    yaml_key: str = "items"
    model: type[T] | None = None
    unique_key_fn: Callable[[Any], Any] | None = None
    unique_name: str = "item"

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._items: list[T] = []
        self.invalid_count: int = 0  # NEW
        self.last_loaded_at: datetime | None = None  # NEW

    @classmethod
    async def create(cls, file_path: Path) -> "BaseYamlRepo[T]":
        self = cls.__new__(cls)
        self.file_path = Path(file_path)
        self._items = await self._load_items()
        return self

    async def _load_items(self) -> list[T]:
        """Load YAML dan validasi isi."""
        if not self.file_path.exists():
            logger.error(f"[YAML Repo] File tidak ditemukan: {self.file_path}")
            raise AppException.YamlFileNotFoundError(str(self.file_path))

        try:
            async with aiofiles.open(self.file_path) as f:
                content = await f.read()
                data = yaml.safe_load(content) or {}

            raw_items = data.get(self.yaml_key, [])
            if self.unique_key_fn:
                validate_unique(raw_items, self.unique_key_fn, name=self.unique_name)

            if self.model is None:
                raise AppException.ModelNotSetError()

            valid_items = []
            invalid_count = 0

            for idx, raw in enumerate(raw_items):
                try:
                    item = self.model(**raw)
                    valid_items.append(item)
                except Exception as e:
                    logger.warning(
                        f"[YAML Repo] {self.unique_name} #{idx} invalid: {e}"
                    )
                    invalid_count += 1

            logger.info(
                f"Loaded {len(valid_items)} {self.yaml_key} dari {self.file_path}"
            )
            self.invalid_count = invalid_count
            self.last_loaded_at = datetime.now()
            return valid_items

        except Exception:
            logger.exception(f"[YAML Repo] Gagal load dari {self.file_path}")
            raise

    def all(self) -> tuple[T, ...]:
        return tuple(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def get_by(self, key_fn: Callable[[T], Any], value: Any) -> T:
        for item in self._items:
            if key_fn(item) == value:
                return item
        raise AppException.ItemNotFoundError(self.unique_name, value)
