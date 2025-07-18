# src/routers/transaction.py
from fastapi import APIRouter, Depends, Request
from src.config.log_settings import logger
from src.dependencies.ip_guard import ip_whitelist_guard
from src.dependencies.module_validator import get_valid_active_module
from src.schemas.sch_transaction import TrxRequest

router = APIRouter()


@router.get("/trx", dependencies=[Depends(ip_whitelist_guard)])
@router.get(
    "/trx/{module_code}", dependencies=[Depends(ip_whitelist_guard)]
)  # Tambahkan ip_whitelist_guard juga di sini
async def transasaction_handler(
    request: Request,
    module_code=Depends(get_valid_active_module),  # noqa: B008
    query: TrxRequest = Depends(),
):
    """Get transaction details."""
    logger.info(
        f"Received request for transaction with module_code: {getattr(module_code, 'moduleid', module_code)}"
    )

    # Simulate fetching transaction data
    transaction_data = {
        "module_code": getattr(module_code, "moduleid", module_code),
        "query": query.model_dump(),
        "status": "success",
        "message": "Transaction details fetched successfully",
    }

    return transaction_data
