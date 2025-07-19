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
from src.services.accept_response import ResponseHandler
from src.services.send_request import RequestForwarder
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
    # lagi bangun query
    final_query = build_final_query(request, module, valid_mapping, query)
    # forward ke target URL
    logger.info(f"[TRX] Final query: {final_query}")
    # Forward
    forwarder = RequestForwarder(module)
    raw_response = await forwarder.send(final_query)

    # Parse
    parsed_response = ResponseHandler.parse(raw_response)

    return {
        "module_code": module.moduleid,
        "memberid": member.memberid,
        "product_code": product.code,
        "signature": valid_signature,
        "query": query.model_dump(),
        "final_query": final_query,
        "response": parsed_response,
        "status": "success",
        "message": "Transaction handled with full validation and query built",
    }
