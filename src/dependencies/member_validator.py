from fastapi import HTTPException, Request

from src.repos.rep_member import MemberRepoYaml
from src.schemas.sch_base_member import Member  # atau schema yg lu pake
from src.utils.mylogger import logger  # tambahkan import logger

member_repo = MemberRepoYaml()


def get_valid_member(request: Request, member_id: str) -> Member:
    logger.info(
        f"Validasi member_id={member_id} dari IP={request.client.host if request.client else 'unknown'}"
    )
    member = member_repo.get_by_memberid(member_id)
    if not member:
        logger.warning(f"Member {member_id} tidak ditemukan")
        raise HTTPException(status_code=404, detail="Member tidak ditemukan")

    if not member.is_active:
        logger.warning(f"Member {member_id} tidak aktif")
        raise HTTPException(status_code=403, detail="Member tidak aktif")

    if request.client is None or request.client.host is None:
        logger.error("Tidak dapat mengambil IP client")
        raise HTTPException(status_code=400, detail="Tidak dapat mengambil IP client")

    ip = request.client.host
    if member.ip != ip:
        logger.warning(
            f"IP tidak cocok untuk member {member_id}: expected {member.ip}, got {ip}"
        )
        raise HTTPException(status_code=403, detail="IP tidak cocok")

    logger.info(f"Member {member_id} valid dan aktif dari IP {ip}")
    return member
