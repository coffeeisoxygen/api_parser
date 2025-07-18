"""This module defines custom exceptions for repository operations.

These exceptions are used to handle specific error cases related to YAML file operations and item retrieval.

- YamlFileNotFoundError: Raised when a required YAML file is missing.
- ItemNotFoundError: Raised when a requested item is not found in the repository.
"""

from typing import Any

from src.exceptions.app_exceptions import AppExceptionError


class YamlFileNotFoundError(AppExceptionError):
    """Raised when a required YAML file is not found on disk."""

    def __init__(self, path: str):
        super().__init__(
            status_code=500, context={"message": f"YAML file tidak ditemukan: {path}"}
        )


class ItemNotFoundError(AppExceptionError):
    """Raised when a requested item is not found in the repository."""

    def __init__(self, item_name: str, value: str):
        message = f"{item_name} dengan nilai '{value}' tidak ditemukan"
        super().__init__(status_code=404, context={"message": message})


class ModelNotSetError(RuntimeError):
    """Raised if BaseYamlRepo subclass does not set the model attribute."""

    def __init__(self):
        super().__init__("BaseYamlRepo: 'model' attribute must be set in subclass.")


class DuplicateItemError(Exception):
    def __init__(self, name: str, key: Any):
        super().__init__(f"Duplicate {name}: {key}")
