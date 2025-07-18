from fastapi import APIRouter, Depends
from src.config.log_settings import logger
from src.dependencies import DepValidModule, DepWhitelist
from src.schemas.sch_transaction import TrxRequest

router = APIRouter()


@router.get("/trx")
async def trx_default(_: DepWhitelist, query: TrxRequest = Depends()):  # noqa: B008, D103
    logger.info("TRX Default Handler")
    return {
        "module_code": None,
        "query": query.model_dump(),
        "status": "success",
        "message": "Default transaction handler",
    }


@router.get("/trx/{module_code}")
async def trx_with_module(
    _: DepWhitelist,
    module: DepValidModule,
    query: TrxRequest = Depends(),  # noqa: B008
):
    logger.info(f"TRX With Module: {module.moduleid}")
    return {
        "module_code": module.moduleid,
        "query": query.model_dump(),
        "status": "success",
        "message": "Transaction handled with module",
    }
