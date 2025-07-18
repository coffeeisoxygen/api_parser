# src/dependencies/deps_product.py
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request

from src.dependencies.deps_module import DepValidModule
from src.schemas.sch_product import Product


def _validate_product_module_mapping(
    request: Request,
    module: DepValidModule,  # <- ambil module yg sudah tervalidasi
    product_code: str = Query(..., alias="product"),
) -> Product:
    repo = request.app.state.repos["mapping"]  # mapping = product_module_mapping

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
    return mapping  # mapping schema udah inherit dari Product


DepValidMapping = Annotated[Product, Depends(_validate_product_module_mapping)]
