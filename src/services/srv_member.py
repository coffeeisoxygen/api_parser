"""Service untuk ambil data Member (mirip repo, tapi di level service)."""

from src.exceptions.app_exceptions import AppExceptionError
from src.repos.rep_member import MemberRepoYaml
from src.services.srv_result import ServiceResult

repo = MemberRepoYaml()


class MemberService:
    @staticmethod
    def get_by_id(memberid: str) -> ServiceResult:
        try:
            member = repo.get_by_memberid(memberid)
            if not member:
                raise AppExceptionError.NotFound("Member", memberid)
            return ServiceResult(member)
        except Exception as e:
            return ServiceResult(AppExceptionError.from_exception(e))
