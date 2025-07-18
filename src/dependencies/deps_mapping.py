from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request

from src.dependencies.deps_module import DepValidModule
from src.schemas.sch_mapping import ProductModuleMapping


def _validate_product_module_mapping(
    request: Request,
    module: DepValidModule,
    product_code: str = Query(..., alias="product"),
) -> ProductModuleMapping:
    repo = request.app.state.repos["mapping"]

    mapping = repo.get_by_product_and_module(product_code, module.moduleid)
    if not mapping:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product_code}' tidak ditemukan di module '{module.moduleid}'",
        )
    if not mapping.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"Product '{product_code}' di module '{module.moduleid}' tidak aktif",
        )

    return mapping


DepValidMapping = Annotated[
    ProductModuleMapping, Depends(_validate_product_module_mapping)
]
