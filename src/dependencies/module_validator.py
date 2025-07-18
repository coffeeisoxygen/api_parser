from src.config.base_settings import settings
from src.exceptions.oto_exceptions import OtoException, OtoExceptionError
from src.repos.rep_module import ModuleRepoYaml
from src.utils.mylogger import logger

module_repo = ModuleRepoYaml(settings.module_yaml_path)


def get_valid_active_module(module_code: str):
    logger.debug(f"Validasi module_code: {module_code}")
    module = module_repo.get_by_moduleid(module_code)
    if not module:
        logger.warning(f"Module '{module_code}' tidak ditemukan")
        raise OtoException.ModuleNotFoundError(module_code)
    if not getattr(module, "is_active", False):
        logger.warning(f"Module '{module_code}' tidak aktif")
        raise OtoExceptionError(
            status_code=403,
            context={
                "code": module_code,
                "message": f"Modul dengan kode '{module_code}' tidak aktif.",
            },
        )
    logger.info(f"Module '{module_code}' valid dan aktif")
    return module
