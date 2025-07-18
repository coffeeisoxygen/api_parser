"""repository layer fot member, untuk sekarang kita akan melakukan nya dengan yaml.

dengan di buat repos ketika kita akan berpindah ke database tidak terlalu banyak yang perlu diubah.
"""

from pathlib import Path

from src.config.base_settings import settings
from src.repos.base_repo import BaseYamlRepo
from src.schemas.sch_base_member import Member

# Default path for member YAML file
default_path = settings.member_yaml_path


class MemberRepoYaml(BaseYamlRepo[Member]):
    yaml_key = "members"
    model = Member
    unique_key_fn = staticmethod(lambda x: x["memberid"])
    unique_name = "memberid"

    def __init__(self, file_path: Path = default_path):
        super().__init__(file_path)

    # Base sudah punya generic get_by()
    # tetap definisikan secara eksplisit buat clarity + IDE support
    def get_by_memberid(self, memberid: str) -> Member | None:
        return next((m for m in self._items if m.memberid == memberid), None)

    def get_by_memberip(self, ip: str) -> Member | None:
        return next((m for m in self._items if m.ip == ip), None)

    def get_allmemberip(self) -> list[str]:
        """Get list of unique IPs from members."""
        return list({m.ip for m in self._items if m.ip})


# NOTE: untuk create , update , delete nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
