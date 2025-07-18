# src/routers/router_trx.py

from fastapi import APIRouter, Depends
from src.config.log_settings import logger
from src.dependencies import DepValidMember, DepValidModule, DepWhitelist
from src.dependencies.deps_product import DepValidProduct
from src.schemas.sch_transaction import TrxRequest

router = APIRouter()


@router.get("/trx/{module_code}")
async def trx_with_module(
    _: DepWhitelist,
    module: DepValidModule,
    member: DepValidMember,
    product: DepValidProduct,
    query: TrxRequest = Depends(),
):
    """Handle transaction request dengan validasi module, member, product, whitelist, dan signature."""
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
