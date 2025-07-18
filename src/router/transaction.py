# src/routers/router_trx.py

from fastapi import APIRouter, Depends
from src.config.log_settings import logger
from src.dependencies import (
    DepValidMember,
    DepValidModule,
    DepValidProduct,
    DepValidSignature,
    DepWhitelist,
)
from src.schemas.sch_transaction import TrxRequest

router = APIRouter()


@router.get("/trx")
async def trx_default(
    _: DepWhitelist,
    member: DepValidMember = None,
    product: DepValidProduct = None,
    valid_signature: DepValidSignature = None,
    query: TrxRequest = Depends(),  # noqa: B008
):
    """Handler default trx tanpa module_code (untuk fallback legacy OtomaX)."""
    logger.info("[TRX] Default handler (tanpa module)")
    return {
        "module_code": None,
        "memberid": getattr(member, "memberid", None),
        "product_code": getattr(product, "code", None),
        "query": query.model_dump(),
        "status": "success",
        "message": "Transaction via default handler",
    }


@router.get("/trx/{module_code}")
async def trx_with_module(
    _: DepWhitelist,
    module: DepValidModule,
    member: DepValidMember,
    product: DepValidProduct,
    valid_signature: DepValidSignature,
    query: TrxRequest = Depends(),  # noqa: B008
):
    """Handler trx dengan module_code (direkomendasikan)."""
    logger.info(
        f"[TRX] Module: {module.moduleid}, Member: {member.memberid}, Product: {product.code}"
    )
    return {
        "module_code": module.moduleid,
        "memberid": member.memberid,
        "product_code": product.code,
        "query": query.model_dump(),
        "status": "success",
        "message": "Transaction handled with full validation",
    }
