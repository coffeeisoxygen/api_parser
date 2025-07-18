# src/routers/router_trx.py

from fastapi import APIRouter, Depends
from src.config.log_settings import logger
from src.dependencies import (
    DepValidMapping,
    DepValidMember,
    DepValidModule,
    DepValidProduct,
    DepValidSignature,
    DepWhitelist,
)
from src.schemas.sch_transaction import TrxRequest

router = APIRouter()


@router.get("/trx/{module_code}")
async def trx_with_module(
    _: DepWhitelist,
    module: DepValidModule,
    member: DepValidMember,
    product: DepValidProduct,
    valid_signature: DepValidSignature,
    valid_mapping: DepValidMapping,
    query: TrxRequest = Depends(),
):
    """Handle transaction request dengan validasi module, member, product, whitelist, dan signature."""
    logger.info(
        f"[TRX] Module: {module.moduleid}, Member: {member.memberid}, Product: {product.code}, Query: {query.model_dump()}, Valid Mapping: {valid_mapping}, Status: success"
    )
    return {
        "module_code": module.moduleid,
        "memberid": member.memberid,
        "product_code": product.code,
        "valid_signature": valid_signature,
        "query": query.model_dump(),
        "status": "success",
        "message": "Transaction handled with full validation",
    }
