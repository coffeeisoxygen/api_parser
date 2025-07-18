from fastapi import APIRouter, Depends
from src.dependencies.ip_guard import ip_whitelist_guard
from src.dependencies.trx_validator import validate_trx_request_access

router = APIRouter()


@router.get("/trx", dependencies=[Depends(ip_whitelist_guard)])
@router.get("/trx/{module_code}")
async def handle_trx(trx=Depends(validate_trx_request_access)):
    return trx
