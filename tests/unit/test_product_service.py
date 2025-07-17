from src.exceptions.app_exceptions import AppException
from src.services.srv_product import ProductService
from src.services.srv_result import ServiceResult


def test_find_product_found(module_repo):
    service = ProductService(module_repo)
    result = service.find_product("CLPDATA")
    assert isinstance(result, ServiceResult)
    assert result.success
    assert isinstance(result.data, dict)
    assert "module" in result.data and "product" in result.data
    assert result.data["product"].code == "CLPDATA"


def test_find_product_not_found(module_repo):
    service = ProductService(module_repo)
    result = service.find_product("NOTFOUND")
    assert not result.success
    assert isinstance(result.data, AppException.ProductNotFoundError)
