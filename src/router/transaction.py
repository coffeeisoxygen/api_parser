from fastapi import APIRouter, Depends
from src.dependencies.ip_guard import ip_whitelist_guard

router = APIRouter()


@router.get("/trx", dependencies=[Depends(ip_whitelist_guard)])
async def handle_trx():
    return {"status": "success"}
