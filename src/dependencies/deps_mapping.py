# src/dependencies/deps_mapping.py
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request

from src.dependencies.deps_module import DepValidModule
from src.schemas.sch_product import Product  # atau Mapping kalau schema lo pisah


def _validate_product_module_mapping(
    request: Request,
    module: DepValidModule,
    product_code: str = Query(..., alias="product"),
) -> Product:
    repo = request.app.state.repos["mapping"]
    mapping = repo.get_by_product_and_module(product_code, module.moduleid)

    if not mapping:
        raise HTTPException(
            404,
            f"Product '{product_code}' tidak ditemukan di module '{module.moduleid}'",
        )
    if not mapping.is_active:
        raise HTTPException(
            400, f"Product '{product_code}' di module '{module.moduleid}' tidak aktif"
        )

    return mapping


DepValidMapping = Annotated[Product, Depends(_validate_product_module_mapping)]
