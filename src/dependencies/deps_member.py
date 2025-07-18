# src/dependencies/deps_member.py
from typing import Annotated

from fastapi import Depends, Request

from src.exceptions.oto_exceptions import OtoException
from src.schemas.sch_member import Member
from src.schemas.sch_transaction import TrxRequest


def _validate_member_from_request(
    request: Request,
    query: TrxRequest = Depends(),  # biarkan FastAPI yang inject  # noqa: B008
) -> Member:
    logger = getattr(request.app.state, "logger", None)
    if logger:
        logger.debug(f"VALIDATOR TRIGGERED with query: {query}")
    repo = request.app.state.repos["member"]
    member = repo.get_by_memberid(query.memberid)
    if logger:
        client_ip = request.client.host if request.client else None
        logger.info(
            f"Client IP: {client_ip!r} vs Member IP: {getattr(member, 'ip', None)!r}"
        )
    error_msg = None
    if not member:
        error_msg = f"Member tidak ditemukan: {query.memberid}"
    elif not member.is_active:
        error_msg = f"Member tidak aktif: {member.memberid}"
    elif not (request.client and request.client.host):
        error_msg = "Tidak dapat mengambil IP client"
    elif str(request.client.host) != str(member.ip):
        error_msg = (
            f"IP tidak cocok dengan member: {request.client.host} != {member.ip}"
        )
    if error_msg:
        if logger:
            logger.warning(error_msg)
        raise OtoException.InvalidTrxCombinationError(error_msg)
    if logger:
        logger.info(f"Member valid: {member.memberid}")
    return member


DepValidMember = Annotated[Member, Depends(_validate_member_from_request)]
