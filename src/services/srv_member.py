"""Service untuk ambil data Member (mirip repo, tapi di level service)."""

from src.exceptions.app_exceptions import AppException
from src.repos.rep_member import MemberRepoYaml
from src.services.srv_base import AppService
from src.services.srv_result import ServiceResult


class MemberService(AppService):
    def __init__(self, repo: MemberRepoYaml):
        super().__init__()
        self.repo = repo

    def get_by_id(self, memberid: str) -> ServiceResult:
        member = self.repo.get_by_id(memberid)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(memberid))
        return ServiceResult(member)

    def get_by_ip(self, ip: str) -> ServiceResult:
        member = self.repo.get_by_ip(ip)
        if not member:
            return ServiceResult(AppException.IPNotVerifiedError(ip))
        return ServiceResult(member)

    def all_members(self) -> ServiceResult:
        members = self.repo.all()
        if not members:
            return ServiceResult(AppException.NoMembersFoundError())
        return ServiceResult(members)
