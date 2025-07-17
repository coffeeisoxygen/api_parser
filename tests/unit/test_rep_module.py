import pytest
from src.schemas.sch_module import Module, Product


@pytest.mark.unit
def test_product_item_creation():
    item = Product(
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
    prod = Product(
        code="CLPDATA",
        name="Cek List Paket DATA Telkomsel",
        provider="TELKOMSEL",
        command="listpaket?category=DATA",
    )
    module = Module(
        name="Digipos",
        code="DIGIPOS",
        base_url="http://10.0.0.3:10003/",
        products=[prod],
        timeout=5,
        methode="GET",
        retry=3,
    )
    assert module.name == "Digipos"
    assert module.code == "DIGIPOS"
    assert module.base_url.startswith("http")
    assert len(module.products) == 1
    assert module.products[0].code == "CLPDATA"


@pytest.mark.unit
def test_module_repo_methods(module_repo):
    modules = module_repo.all()
    assert len(modules) == 1
    assert modules[0].code == "DIGIPOS"
    mod = module_repo.get_by_code("DIGIPOS")
    assert mod is not None
    assert mod.name == "Digipos"
    found = module_repo.find_product_by_code("CLPDATA")
    assert found is not None
    module, product = found
    assert module.code == "DIGIPOS"
    assert product.code == "CLPDATA"
    prod_only = module_repo.get_product_only("CLPVSMS")
    assert prod_only is not None
    assert prod_only.code == "CLPVSMS"
    assert module_repo.get_by_code("NOTFOUND") is None
    assert module_repo.get_product_only("NOTFOUND") is None
