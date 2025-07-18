# src/dependencies/deps_member.py
from typing import Annotated

from fastapi import Depends, Request

from src.exceptions.oto_exceptions import OtoException
from src.schemas.sch_member import Member
from src.schemas.sch_transaction import TrxRequest


def _validate_member_from_request(
    request: Request,
    query: TrxRequest = Depends(),  # ambil param dari query (karena pakai GET)
) -> Member:
    logger = getattr(request.app.state, "logger", None)
    if logger:
        logger.debug(f"VALIDATOR TRIGGERED with query: {query}")
    repo = request.app.state.repos["member"]
    member = repo.get_by_memberid(query.memberid)
    if logger:
        logger.debug(f"Member lookup for id '{query.memberid}': {member}")
    if not member:
        if logger:
            logger.warning("Member tidak ditemukan")
        raise OtoException.InvalidTrxCombinationError("Member tidak ditemukan")
    if not member.is_active:
        if logger:
            logger.warning("Member tidak aktif")
        raise OtoException.InvalidTrxCombinationError("Member tidak aktif")
    if request.client is None or request.client.host is None:
        if logger:
            logger.warning("Tidak dapat mengambil IP client")
        raise OtoException.InvalidTrxCombinationError("Tidak dapat mengambil IP client")
    client_ip = request.client.host
    if logger:
        logger.debug(f"Client IP: {client_ip}, Member IP: {member.ip}")
    if client_ip != member.ip:
        if logger:
            logger.warning("IP tidak cocok dengan member")
        raise OtoException.InvalidTrxCombinationError("IP tidak cocok dengan member")
    if logger:
        logger.info(f"Member valid: {member.memberid}")
    return member


DepValidMember = Annotated[Member, Depends(_validate_member_from_request)]
