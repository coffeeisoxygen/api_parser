"""repository layer fot member, untuk sekarang kita akan melakukan nya dengan yaml.

dengan di buat repos ketika kita akan berpindah ke database tidak terlalu banyak yang perlu diubah.
"""

from pathlib import Path

from src.config.app_config import settings
from src.repos.base_repo import BaseYamlRepo
from src.schemas.sch_base_member import Member

# Default path for member YAML file
default_path = settings.member_yaml_path


class MemberRepoYaml(BaseYamlRepo[Member]):
    yaml_key = "members"
    model = Member
    unique_key_fn = staticmethod(lambda x: x["memberid"])
    unique_name = "memberid"

    def __init__(self, file_path: Path = default_path) -> None:
        super().__init__(file_path)

    # Base sudah punya generic get_by()
    # comtoh dengan dynamic get_by
    # self.get_by("memberid", memberid)
    # tetap definisikan secara eksplisit buat clarity + IDE support
    def get_by_memberid(self, memberid: str) -> Member | None:
        """Get a member by their unique member ID.

        This method retrieves a member from the repository using their member ID.

        Args:
            memberid (str): memberid yg ingin diambil
                Contoh: "M001"

        Returns:
            Member | None: Member yang ditemukan atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return next((m for m in self._items if m.memberid == memberid), None)

    def get_list_member(self) -> list[Member]:
        """Get a list of all members.

        This method retrieves all members from the repository as a list.

        Returns:
            list[Member]: Daftar semua anggota.
        """
        return list(self._items)

    def get_list_active_only(self) -> list[Member]:
        """Get a list of all active members only.

        This method retrieves all members from the repository who are currently active as a list.

        Returns:
            list[Member]: Daftar anggota yang aktif.
        """
        return [m for m in self._items if getattr(m, "is_active", False)]

    def get_by_memberip(self, ip: str) -> Member | None:
        """Get a member by their unique IP address.

        This method retrieves a member from the repository using their IP address.

        Args:
            ip (str): ip yang ingin diambil
                Contoh: "192.168.1.1"

        Returns:
            Member | None: Member yang ditemukan atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return next((m for m in self._items if m.ip == ip), None)

    def get_list_memberip(self) -> list[str]:
        """Get a list of all unique IPs from members.

        This method retrieves all unique IP addresses from the members in the repository as a list.

        Returns:
            list[str]: Daftar IP yang ditemukan.
        """
        return list({m.ip for m in self._items if m.ip})

    def get_all_memberip(self) -> list[str] | None:
        """Get all unique IPs from members.

        This method retrieves all unique IP addresses from the members in the repository.

        Returns:
            list[str] | None: Daftar IP yang ditemukan atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return list({m.ip for m in self._items if m.ip}) or None

    def get_all_active_only_member(self) -> list[Member] | None:
        """Get all active members only.

        This method retrieves all members from the repository who are currently active.

        Returns:
            list[Member] | None: Daftar anggota yang aktif atau None jika tidak ada. akan di handle di level service untuk none.
        """
        return [
            m for m in self._items if getattr(m, "is_active", False) is True
        ] or None


# NOTE: untuk create , update , delete nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
