import sys
from pathlib import Path

import pytest
from loguru import logger
from src.repos.rep_member import MemberRepoYaml
from src.repos.rep_module import ModuleRepoYaml


# Auto-configure Loguru untuk test session
@pytest.fixture(scope="session", autouse=True)
def configure_loguru():
    logger.remove()  # Hapus default handler
    logger.add(
        sink=sys.stderr,
        format="<level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG",
        backtrace=True,
        diagnose=True,
        colorize=True,
    )


# Optional: Intercept loguru → caplog (untuk test log)
@pytest.fixture(autouse=True)
def intercept_loguru(caplog):
    handler_id = logger.add(caplog.handler, format="{message}", level="DEBUG")
    yield
    logger.remove(handler_id)


# Path ke YAML dummy untuk test
@pytest.fixture(scope="session")
def dummy_member_path() -> Path:
    return Path("tests/data/members_dummy.yaml")


# Repo dengan data dummy
@pytest.fixture()
def member_repo(dummy_member_path) -> MemberRepoYaml:
    return MemberRepoYaml(file_path=dummy_member_path)


# path ke Yaml dummy untuk modul dan produk
@pytest.fixture(scope="session")
def dummy_module_path() -> Path:
    return Path("tests/data/modules_dummy.yaml")


# Repo dengan data dummy untuk modul dan produk
@pytest.fixture()
def module_repo(dummy_module_path) -> ModuleRepoYaml:
    return ModuleRepoYaml(file_path=dummy_module_path)
