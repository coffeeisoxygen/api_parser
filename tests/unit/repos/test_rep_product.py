import pytest
from pydantic import ValidationError
from src.schemas.sch_product import Product


def test_get_by_code(product_repo):
    result = product_repo.get_by_code("CLPDATA")
    assert result is None or isinstance(result, Product)
    if result:
        assert result.code == "CLPDATA"


def test_get_list_product(product_repo):
    result = product_repo.get_list_product()
    assert isinstance(result, list)
    assert all(isinstance(p, Product) for p in result)
    assert len(result) >= 1


def test_get_list_active_only(product_repo):
    result = product_repo.get_list_active_only()
    assert isinstance(result, list)
    assert all(getattr(p, "is_active", False) for p in result)


def test_get_by_provider(product_repo):
    result = product_repo.get_by_provider("TELKOMSEL")
    assert isinstance(result, list)
    assert all(p.provider == "TELKOMSEL" for p in result)


def test_get_by_provider_not_found(product_repo):
    result = product_repo.get_by_provider("NONEXISTENT")
    assert isinstance(result, list)
    assert result == []


def test_get_list_provider(product_repo):
    result = product_repo.get_list_provider()
    assert isinstance(result, list)
    assert "TELKOMSEL" in result


def test_product_schema_valid():
    p = Product(code="P001", name="Produk Test", provider="TELKOMSEL", is_active=True)
    assert p.code == "P001"
    assert p.is_active is True


def test_product_schema_invalid():
    with pytest.raises(ValidationError):
        Product(code=None, name=123, provider=None, is_active="yes")  # type: ignore
