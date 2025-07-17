from src.exceptions.app_exceptions import AppException
from src.services.srv_module import ModuleService
from src.services.srv_result import ServiceResult


def test_all_modules(module_repo):
    service = ModuleService(module_repo)
    result = service.all_modules()
    assert isinstance(result, ServiceResult)
    assert result.success
    assert isinstance(result.data, list)
    assert len(result.data) > 0
    assert hasattr(result.data[0], "code")  # Ensure code attribute exists
    assert result.data[0].code == "DIGIPOS"


def test_get_by_code_found(module_repo):
    service = ModuleService(module_repo)
    result = service.get_by_code("DIGIPOS")
    assert result.success
    assert result.data is not None
    assert hasattr(result.data, "code")
    assert result.data.code == "DIGIPOS" # type: ignore


def test_get_by_code_not_found(module_repo):
    service = ModuleService(module_repo)
    result = service.get_by_code("NOTFOUND")
    assert not result.success
    assert isinstance(result.data, AppException.ModuleNotFoundError)
