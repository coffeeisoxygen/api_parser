# src/services/srv_module.py
from src.config.base_settings import settings
from src.exceptions.oto_exceptions import OtoException, OtoExceptionError
from src.repos.rep_module import ModuleRepoYaml
from src.services.srv_base import AppService
from src.services.srv_result import ServiceResult


class ModuleService(AppService):
    def __init__(self, repo: ModuleRepoYaml | None = None):
        super().__init__()
        self.repo = repo or ModuleRepoYaml(settings.module_yaml_path)

    def get_valid_active(self, code: str) -> ServiceResult:
        module = self.repo.get_by_moduleid(code)
        if not module:
            return ServiceResult(OtoException.ModuleNotFoundError(code))
        if not getattr(module, "is_active", False):
            return ServiceResult(
                OtoExceptionError(
                    status_code=403,
                    context={"code": code, "message": f"Modul '{code}' tidak aktif."},
                )
            )
        return ServiceResult(module)
