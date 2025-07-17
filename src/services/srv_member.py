"""Service logic untuk validasi dan akses member."""

from src.exceptions.app_exceptions import AppException
from src.repos.rep_member import MemberRepoYaml
from src.services.srv_base import AppService
from src.services.srv_result import ServiceResult


class MemberService(AppService):
    def __init__(self, repo: MemberRepoYaml):
        super().__init__()
        self.repo = repo

    def get_by_ip(self, ip: str) -> ServiceResult:
        self.logger.debug(f"get_by_ip called with ip={ip}")
        member = self.repo.get_by_ip(ip)
        if not member:
            self.logger.warning(f"No member found for IP: {ip}")
            return ServiceResult(AppException.IPNotVerifiedError(ip))
        return ServiceResult(member)

    def get_by_id(self, memberid: str) -> ServiceResult:
        self.logger.debug(f"get_by_id called with memberid={memberid}")
        member = self.repo.get_by_id(memberid)
        if not member:
            self.logger.warning(f"No member found for memberid: {memberid}")
            return ServiceResult(AppException.MemberNotFoundError(memberid))
        return ServiceResult(member)

    def verify_pin_password(
        self, memberid: str, pin: str, password: str
    ) -> ServiceResult:
        self.logger.debug(f"verify_pin_password called for memberid={memberid}")
        member = self.repo.get_by_id(memberid)
        if not member:
            self.logger.warning(f"Member not found for memberid={memberid}")
            return ServiceResult(AppException.MemberNotFoundError(memberid))
        if member.pin != pin or member.password != password:
            self.logger.warning(f"PIN/password mismatch for memberid={memberid}")
            return ServiceResult(AppException.InvalidCredentialsError(memberid))
        self.logger.info(f"PIN/password verified for memberid={memberid}")
        return ServiceResult(member)

    def is_signature_required(self, memberid: str) -> ServiceResult:
        self.logger.debug(f"is_signature_required called for memberid={memberid}")
        member = self.repo.get_by_id(memberid)
        if not member:
            self.logger.warning(f"Member not found for memberid={memberid}")
            return ServiceResult(AppException.MemberNotFoundError(memberid))
        result = not member.allow_no_sign
        if result:
            self.logger.info(f"Signature required for memberid={memberid}: {result}")
            return ServiceResult(True)
        else:
            self.logger.info(f"No signature required for memberid={memberid}")
            return ServiceResult(False)

    def get_report_url(self, memberid: str) -> ServiceResult:
        self.logger.debug(f"get_report_url called for memberid={memberid}")
        member = self.repo.get_by_id(memberid)
        if not member:
            self.logger.warning(f"Member not found for memberid={memberid}")
            return ServiceResult(AppException.MemberNotFoundError(memberid))
        url = member.report_url or f"http://{member.ip}/report"
        if not url:
            self.logger.warning(f"Report URL not found for memberid={memberid}")
            return ServiceResult(AppException.ReportUrlNotFoundError(memberid))
        self.logger.info(f"Report URL for memberid={memberid}: {url}")
        return ServiceResult(url)

    def all_members(self) -> ServiceResult:
        self.logger.debug("all_members called")
        members = self.repo.all()
        if not members:
            self.logger.warning("No members found in repository")
            return ServiceResult(AppException.NoMembersFoundError())
        self.logger.info(f"Total members fetched: {len(members)}")
        return ServiceResult(members)
