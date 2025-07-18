"""load ipaddress dari members dan modules untuk whitelist ip yg bisa akses , dan akan di terapkan di level router."""

from urllib.parse import urlparse

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
            self.logger.info(f"Fetched member IPs: {member_ips}")
            module_urls = self.module_repo.get_all_module_listip() or []
            self.logger.info(f"Fetched module URLs: {module_urls}")
            # Ekstrak hanya host/IP dari base_url
            module_ips = []
            for url in module_urls:
                if url:
                    parsed = urlparse(url)
                    if parsed.hostname:
                        module_ips.append(parsed.hostname)
                        self.logger.info(
                            f"Extracted hostname from module URL '{url}': {parsed.hostname}"
                        )
                    else:
                        module_ips.append(url)  # fallback jika bukan URL
                        self.logger.info(
                            f"Module URL '{url}' is not a valid URL, using as is."
                        )
            all_ip = list(set(member_ips + module_ips))
            self.logger.info(f"Combined whitelist IPs: {all_ip}")
            if not all_ip:
                return ServiceResult(
                    AppException.IPNotFoundError("Tidak ada IP yang ditemukan")
                )
            return ServiceResult(all_ip)
        except Exception as e:
            self.logger.exception("Gagal ambil list IP whitelist")
            return ServiceResult(AppException.IPNotFoundError(str(e)))
