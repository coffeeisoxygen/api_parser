"""schemas untuk crud member, untuk sekarang kita akan melakukan nya dengan yaml."""

from pydantic import BaseModel, Field


class Member(BaseModel):
    model_config = {
        "from_attributes": True,
        "str_strip_whitespace": True,
        "extra": "forbid",  # strict: hanya field yang didefinisikan
    }
    memberid: str = Field(..., description="ID unik member")
    password: str = Field(..., description="Password member")
    pin: str = Field(..., description="PIN member")
    ip: str = Field(..., description="IP address member")
    report_url: str | None = Field(None, description="URL untuk report, bisa null")
    allow_no_sign: bool = Field(..., description="Apakah diperbolehkan tanpa sign")
    is_active: bool = Field(default=True, description="Apakah member aktif")


# NOTE: field validator dan model validator nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
