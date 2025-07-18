from fastapi import APIRouter, Depends
from src.dependencies.ip_guard import ip_whitelist_guard
from src.dependencies.module_validator import get_valid_active_module
from src.schemas.sch_transaction import TrxRequestQuery

router = APIRouter()


@router.get("/trx", dependencies=[Depends(ip_whitelist_guard)])
@router.get("/trx/{module_code}")
async def handle_trx(
    module_code=Depends(get_valid_active_module),  # noqa: ANN001, B008
    query: TrxRequestQuery = Depends(),  # noqa: B008
):
    # Di titik ini: query sudah tervalidasi (product, qty, refid, dst)
    return {"ok": True, "module": module_code, "query": query}
