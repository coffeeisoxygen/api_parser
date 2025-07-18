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


# src/routers/router_trx.py


@router.get("/trx")
async def trx_default(_: DepWhitelist, query: TrxRequest = Depends()):
    logger.info("[TRX] Default handler (tanpa module)")
    return {
        "module_code": None,
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
    query: TrxRequest = Depends(),
):
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
