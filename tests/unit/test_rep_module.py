import pytest
from src.schemas.sch_module import ModuleItem, ProductItem


@pytest.mark.unit
def test_product_item_creation():
    item = ProductItem(
        code="CLPDATA",
        name="Cek List Paket DATA Telkomsel",
        provider="TELKOMSEL",
        command="listpaket?category=DATA",
    )
    assert item.code == "CLPDATA"
    assert item.name.startswith("Cek List Paket")
    assert item.provider == "TELKOMSEL"
    assert "category=DATA" in item.command


@pytest.mark.unit
def test_module_item_creation():
    prod = ProductItem(
        code="CLPDATA",
        name="Cek List Paket DATA Telkomsel",
        provider="TELKOMSEL",
        command="listpaket?category=DATA",
    )
    module = ModuleItem(
        name="Digipos",
        code="DIGIPOS",
        base_url="http://10.0.0.3:10003/",
        products=[prod],
    )
    assert module.name == "Digipos"
    assert module.code == "DIGIPOS"
    assert module.base_url.startswith("http")
    assert len(module.products) == 1
    assert module.products[0].code
