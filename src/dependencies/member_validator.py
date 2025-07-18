from fastapi import HTTPException, Request

from src.repos.rep_member import MemberRepoYaml
from src.schemas.sch_base_member import Member  # atau schema yg lu pake

member_repo = MemberRepoYaml()


def get_valid_member(request: Request, member_id: str) -> Member:
    member = member_repo.get_by_memberid(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member tidak ditemukan")

    if not member.is_active:
        raise HTTPException(status_code=403, detail="Member tidak aktif")

    if request.client is None or request.client.host is None:
        raise HTTPException(status_code=400, detail="Tidak dapat mengambil IP client")

    ip = request.client.host
    if member.ip != ip:
        raise HTTPException(status_code=403, detail="IP tidak cocok")

    return member
