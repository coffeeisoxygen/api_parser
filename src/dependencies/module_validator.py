# from fastapi import Depends, Path

# from src.exceptions.oto_exceptions import OtoException
# from src.services.srv_module_validation import ModuleService


# def get_module_service() -> ModuleService:
#     """Dependency provider untuk ModuleService."""
#     return ModuleService()


# def get_valid_active_module(
#     module_code: str = Path(..., description="Kode modul aktif"),
#     module_service: ModuleService = Depends(get_module_service),  # noqa: B008
# ):
#     """Dependency untuk validasi module aktif, raise OtoExceptionError jika tidak valid."""
#     result = module_service.get_valid_active(module_code)
#     if not result.success:
#         if result.error:
#             raise result.error
#         else:
#             raise OtoException.UnknownModuleValidationError(module_code)
#     return result.data
