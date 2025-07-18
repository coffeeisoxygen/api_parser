# src/dependencies/deps_product.py
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request

from src.schemas.sch_product import Product


def _validate_product_from_repo(
    request: Request, product_code: str = Query(..., alias="product")
) -> Product:
    repo = request.app.state.repos["product"]
    product = repo.get_by_product_code(product_code)

    if not product:
        raise HTTPException(404, f"Product '{product_code}' tidak ditemukan")
    if not product.is_active:
        raise HTTPException(400, f"Product '{product_code}' tidak aktif")

    return product


DepValidProduct = Annotated[Product, Depends(_validate_product_from_repo)]
