"""Base class for YAML repository loaders with uniqueness validation and logging."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, Generic, TypeVar

import yaml

from src.repos.rep_helper import validate_unique
from src.utils.mylogger import logger

T = TypeVar("T")


class BaseYamlRepo(Generic[T]):
    yaml_key: str = "items"  # override in subclass
    model: type[T] = None  # override in subclass
    unique_key_fn: Callable[[Any], Any] = None  # override in subclass
    unique_name: str = "item"  # override in subclass

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._items = self._load_items()

    def _load_items(self) -> list[T]:
        if not self.file_path.exists():
            logger.warning(f"YAML file not found: {self.file_path}")
            return []
        with self.file_path.open("r") as f:
            data = yaml.safe_load(f) or {}
        raw_items = data.get(self.yaml_key, [])
        try:
            if self.unique_key_fn:
                validate_unique(raw_items, self.unique_key_fn, name=self.unique_name)
        except Exception as e:
            logger.error(f"Failed to load {self.yaml_key}: {e}")
            raise
        logger.info(f"Loaded {len(raw_items)} {self.yaml_key} from {self.file_path}")
        return [self.model(**item) for item in raw_items]

    def all(self) -> list[T]:
        return self._items.copy()
