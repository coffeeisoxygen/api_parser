import pytest
from src.repos.rep_mapping import MappingRepoYaml
from src.schemas.sch_base_mappings import ProductModuleMapping


@pytest.mark.unit
def test_get_by_product(mapping_repo: MappingRepoYaml):
    result = mapping_repo.get_by_product("CLPDATA")
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, ProductModuleMapping)


@pytest.mark.unit
def test_get_by_module(mapping_repo: MappingRepoYaml):
    result = mapping_repo.get_by_module("DIGIPOS")
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, ProductModuleMapping)


@pytest.mark.unit
def test_get_list_active_only(mapping_repo: MappingRepoYaml):
    result = mapping_repo.get_list_active_only()
    assert isinstance(result, list)
    for item in result:
        assert getattr(item, "is_active", False)


@pytest.mark.unit
def test_get_list_mapping(mapping_repo: MappingRepoYaml):
    result = mapping_repo.get_list_mapping()
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, ProductModuleMapping)
