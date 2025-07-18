import pytest
from pydantic import ValidationError
from src.schemas.sch_base_modules import Module


def test_get_by_moduleid(module_repo):
    result = module_repo.get_by_moduleid("M001")
    assert result is None or isinstance(result, Module)


def test_get_all_module_listip(module_repo):
    result = module_repo.get_all_module_listip()
    assert result is None or isinstance(result, list)
    if result:
        assert all(isinstance(ip, str) for ip in result)


def test_get_all_active_only_module(module_repo):
    result = module_repo.get_all_active_only_module()
    assert result is None or isinstance(result, list)
    if result:
        assert all(getattr(m, "is_active", False) for m in result)


def test_get_list_module(module_repo):
    result = module_repo.get_list_module()
    assert isinstance(result, list)
    assert all(isinstance(m, Module) for m in result)


def test_get_list_active_only(module_repo):
    result = module_repo.get_list_active_only()
    assert isinstance(result, list)
    assert all(getattr(m, "is_active", False) for m in result)


def test_get_by_moduleip(module_repo):
    # Use an IP from your actual test data if available
    result = module_repo.get_by_moduleip("http://localhost/")
    assert result is None or isinstance(result, Module)


def test_get_list_moduleip(module_repo):
    result = module_repo.get_list_moduleip()
    assert isinstance(result, list)
    assert all(isinstance(ip, str) for ip in result)


def test_module_schema_valid():
    m = Module(
        moduleid="M001",
        name="Test Module",
        description="This is a test module.",
        timeout=30,
        method="GET",
        retry=3,
        wait_seconds=5,
        parameters={"key": "value"},
        base_url="http://localhost/",
        is_active=True,
    )
    assert m.moduleid == "M001"
    assert m.is_active is True


def test_module_schema_invalid():
    with pytest.raises(ValidationError):
        Module(moduleid="M001", name=None, description=123, timeout="thirty", method="INVALID", retry="three", wait_seconds="five", parameters="not_a_dict", base_url=None, is_active="yes")
