from typing import Annotated

from fastapi import Depends, HTTPException, Request


def _check_ip_whitelist(request: Request):
    client_ip = request.client.host if request.client else None
    logger = getattr(request.app.state, "logger", None)
    if not client_ip:
        if logger:
            logger.warning("Tidak dapat menentukan IP client")
        raise HTTPException(400, detail="Tidak dapat menentukan IP client")

    member_repo = request.app.state.repos["member"]
    module_repo = request.app.state.repos["module"]

    whitelist = set(member_repo.get_all_memberip() or []) | set(
        module_repo.get_all_module_listip() or []
    )

    if client_ip not in whitelist:
        if logger:
            logger.warning(f"IP '{client_ip}' tidak diizinkan")
        raise HTTPException(403, detail=f"IP '{client_ip}' tidak diizinkan")
    else:
        if logger:
            logger.info(f"IP '{client_ip}' diizinkan mengakses endpoint")


DepWhitelist = Annotated[None, Depends(_check_ip_whitelist)]
