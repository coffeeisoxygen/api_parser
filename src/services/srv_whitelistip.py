"""load ipaddress dari members dan modules untuk whitelist ip yg bisa akses , dan akan di terapkan di level router."""

from src.exceptions.app_exceptions import AppException
from src.repos.rep_member import MemberRepoYaml
from src.repos.rep_module import ModuleRepoYaml
from src.services.srv_base import AppService
from src.services.srv_result import ServiceResult


class WhitelistIPService(AppService):
    def __init__(self, member_repo: MemberRepoYaml, module_repo: ModuleRepoYaml):
        super().__init__()
        self.member_repo = member_repo
        self.module_repo = module_repo

    def get_all_ip(self) -> ServiceResult:
        try:
            member_ips = self.member_repo.get_all_memberip() or []
            module_ips = self.module_repo.get_all_module_listip() or []
            all_ip = list(set(member_ips + module_ips))
            if not all_ip:
                return ServiceResult(
                    AppException.IPNotFoundError("Tidak ada IP yang ditemukan")
                )
            return ServiceResult(all_ip)
        except Exception as e:
            self.logger.exception("Gagal ambil list IP whitelist")
            return ServiceResult(AppException.IPNotFoundError(str(e)))
