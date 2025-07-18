# src/routers/router_trx.py

from fastapi import APIRouter, Depends, Request
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
from src.services.srv_query_builder import build_final_query

router = APIRouter()


@router.get("/trx/{module_code}")
async def trx_with_module(
    request: Request,
    _: DepWhitelist,
    module: DepValidModule,
    member: DepValidMember,
    product: DepValidProduct,
    valid_signature: DepValidSignature,
    valid_mapping: DepValidMapping,
    query: TrxRequest = Depends(),
):
    """Handle transaction request dengan validasi lengkap (module, member, product, signature)."""
    logger.info(
        f"[TRX] Module: {module.moduleid}, Member: {member.memberid}, Product: {product.code}"
    )
    logger.info(f"[TRX] Raw query: {query.model_dump()}")

    logger.info("[FORWARD_TEST] Membangun final query...")
    final_query = build_final_query(request, module, valid_mapping, query)

    return {
        "module_code": module.moduleid,
        "memberid": member.memberid,
        "product_code": product.code,
        "query": query.model_dump(),
        "final_query": final_query,
        "status": "success",
        "message": "Transaction handled with full validation and query built",
    }
