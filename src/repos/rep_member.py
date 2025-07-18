"""repository layer fot member, untuk sekarang kita akan melakukan nya dengan yaml.

dengan di buat repos ketika kita akan berpindah ke database tidak terlalu banyak yang perlu diubah.
"""

from pathlib import Path

import yaml

from src.config.base_settings import settings
from src.repos.rep_helper import validate_unique
from src.schemas.sch_base_member import Member
from src.utils.mylogger import logger

# Default path for member YAML file
DEFAULT_PATH = settings.member_yaml_path


class MemberRepoYaml:
    def __init__(self, file_path: Path = DEFAULT_PATH):
        self.file_path = Path(file_path)
        self._members = self._load_members()

    def _load_members(self) -> list[Member]:
        if not self.file_path.exists():
            logger.warning(f"Member file not found: {self.file_path}")
            return []

        with self.file_path.open("r") as f:
            data = yaml.safe_load(f) or {}

        raw_members = data.get("members", [])
        try:
            validate_unique(raw_members, lambda x: x["memberid"], name="memberid")
        except Exception as e:
            logger.error(f"Failed to load members: {e}")
            raise
        logger.info(f"Loaded {len(raw_members)} members from {self.file_path}")
        return [Member(**item) for item in raw_members]

    def get_by_ip(self, ip: str) -> Member | None:
        return next((m for m in self._members if m.ip == ip), None)

    def get_by_id(self, memberid: str) -> Member | None:
        return next((m for m in self._members if m.memberid == memberid), None)

    def get_listip(self) -> list[str]:
        """Get list of unique IPs from members."""
        return list({m.ip for m in self._members if m.ip})

    def all(self) -> list[Member]:
        return self._members.copy()  # return copy supaya aman dari modifikasi eksternal


# NOTE: untuk create , update , delete nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
