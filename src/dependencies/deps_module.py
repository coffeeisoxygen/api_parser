from typing import Annotated

from fastapi import Depends, HTTPException, Path, Request

from src.schemas.sch_module import Module


def _validate_module_from_path(
    request: Request, module_code: str = Path(...)
) -> Module:
    repo = request.app.state.repos["module"]
    module = repo.get_by_moduleid(module_code)

    if not module:
        raise HTTPException(404, detail=f"Module '{module_code}' tidak ditemukan")
    if not module.is_active:
        raise HTTPException(400, detail=f"Module '{module_code}' tidak aktif")

    return module


DepValidModule = Annotated[Module, Depends(_validate_module_from_path)]
