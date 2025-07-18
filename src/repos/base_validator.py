"""karena kita pake yaml, jadi kita tidka bisa enforce validasiseperti database , jadi kita kana membuat base loader, yg akan di pakai oleh repo masing masing."""

from collections.abc import Callable, Iterable
from typing import Any

from src.exceptions.repo_exceptions import DuplicateItemError


def validate_unique(
    items: Iterable[Any], key_fn: Callable[[Any], Any], name: str = "item"
):
    """Validate that all items in the iterable are unique based on a key function.

    This function checks that no two items in the iterable have the same key
    as determined by the key function. If a duplicate is found, a ValueError
    is raised.

    Args:
        items (Iterable[Any]): The items to check for uniqueness.
        key_fn (Callable[[Any], Any]): A function that extracts the key from each item.
        name (str, optional): A name for the items, used in the error message. Defaults to "item".

    Raises:
        ValueError: If duplicate items are found.
    """
    seen = set()
    for item in items:
        key = key_fn(item)
        if key in seen:
            raise DuplicateItemError(name, key)
        seen.add(key)
