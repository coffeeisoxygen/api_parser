from fastapi import Path

from src.services.srv_module import ModuleService

module_service = ModuleService()


def get_valid_active_module(
    module_code: str = Path(..., description="Kode modul aktif"),
):
    result = module_service.get_valid_active(module_code)
    if not result.success:
        # Anggap result.error sudah turunan OtoExceptionError
        raise result.error
    return result.data
