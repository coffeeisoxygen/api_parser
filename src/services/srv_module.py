from src.exceptions.app_exceptions import AppException
from src.repos.rep_module import ModuleRepoYaml
from src.services.srv_base import AppService
from src.services.srv_result import ServiceResult


class ModuleService(AppService):
    def __init__(self, repo: ModuleRepoYaml):
        super().__init__()
        self.repo = repo

    def get_by_code(self, code: str) -> ServiceResult:
        self.logger.debug(f"get_by_code called with code={code}")
        module = self.repo.get_by_code(code)
        if module is not None:
            return ServiceResult(module)
        else:
            return ServiceResult(AppException.ModuleNotFoundError(code))

    def all_modules(self) -> ServiceResult:
        self.logger.debug("all_modules called")
        modules = self.repo.all()
        return ServiceResult(modules)
