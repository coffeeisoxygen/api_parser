"""BaseYamlRepo: Base generic loader untuk YAML-based repository.

Fitur:
- Load dan validasi uniqueness field
- Raise exception kalau file/data not exist
- Siap di-extend oleh semua repo
- Komentar untuk future: reload/watch mode

By: Hasan Maki & ChatGPT ❤️
"""

from collections.abc import Callable
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
    yaml_key: str = "items"  # Key di dalam YAML
    model: type[T] | None = None  # Pydantic model
    unique_key_fn: Callable[[Any], Any] | None = None  # Fungsi ambil key unik
    unique_name: str = "item"  # Untuk error message

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._items: list[T] = []  # Inisialisasi kosong, isi di method async

    @classmethod
    async def create(cls, file_path: Path) -> "BaseYamlRepo[T]":
        self = cls.__new__(cls)
        self.file_path = Path(file_path)
        self._items = await self._load_items()
        return self

    async def _load_items(self) -> list[T]:
        """Load YAML secara async dan validasi item.

        Raises:
            YamlFileNotFoundError: Jika file YAML tidak ditemukan.
            ModelNotSetError: Jika model belum di-set di subclass.
            Exception: Jika validasi uniqueness gagal atau parsing error.
        """
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

            logger.info(
                f"Loaded {len(raw_items)} {self.yaml_key} dari {self.file_path}"
            )

            if self.model is None:
                raise AppException.ModelNotSetError()
            return [self.model(**item) for item in raw_items]
        except Exception:
            logger.exception(f"[YAML Repo] Gagal load dari {self.file_path}")
            raise

    def all(self) -> tuple[T, ...]:
        """Return semua item (immutable tuple)."""
        return tuple(self._items)

    def __len__(self) -> int:
        """Return jumlah item."""
        return len(self._items)

    def __iter__(self):
        """Iterate semua item."""
        return iter(self._items)

    def get_by(self, key_fn: Callable[[T], Any], value: Any) -> T:
        """Generic getter (return 1 item), raise ItemNotFoundError kalau tidak ketemu.

        Args:
            key_fn: Fungsi untuk mengambil key dari item.
            value: Nilai yang dicari.

        Raises:
            ItemNotFoundError: Jika item tidak ditemukan.
        """
        for item in self._items:
            if key_fn(item) == value:
                return item
        raise ItemNotFoundError(self.unique_name, value)

    # ✳️ optional future:
    # async def reload(self): self._items = await self._load_items()
