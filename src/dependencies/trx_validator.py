from fastapi import Depends, HTTPException, Request

from src.dependencies.member_validator import get_valid_member
from src.dependencies.module_validator import get_valid_active_module
from src.schemas.sch_base_member import Member
from src.schemas.sch_transaction import TrxRequestQuery


def validate_trx_request_access(
    request: Request,
    module=Depends(get_valid_active_module),  # noqa: B008
    query: TrxRequestQuery = Depends(),  # noqa: B008
    member: Member = Depends(get_valid_member),  # noqa: B008
) -> dict:
    """Validasi kombinasi member, module, dan query untuk transaksi."""
    if member.allow_no_sign:
        if not (query.pin and query.pass_):
            raise HTTPException(
                status_code=422, detail="pin dan pass wajib jika allow_no_sign = True"
            )
    else:
        if not query.sign:
            raise HTTPException(
                status_code=422, detail="sign wajib jika allow_no_sign = False"
            )
    return {"ok": True, "module": module, "member": member, "query": query}
