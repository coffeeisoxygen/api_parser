from src.exceptions.app_exceptions import AppException
from src.repos.rep_module import ModuleRepoYaml
from src.services.srv_base import AppService
from src.services.srv_result import ServiceResult


class ProductService(AppService):
    def __init__(self, repo: ModuleRepoYaml):
        super().__init__()
        self.repo = repo

    def find_product(self, product_code: str) -> ServiceResult:
        self.logger.debug(f"find_product called with code={product_code}")
        result = self.repo.find_product_by_code(product_code)
        if not result:
            return ServiceResult(AppException.ProductNotFoundError(product_code))
        module, product = result
        return ServiceResult({"module": module, "product": product})
