"""schema untuk member yang akan consume API middleware."""

from pydantic import BaseModel, Field, field_validator


class Member(BaseModel):
    model_config = {
        "from_attributes": True,
        "str_strip_whitespace": True,
        "extra": "forbid",
    }

    memberid: str = Field(description="ID Requester")
    password: str = Field(description="Password Requester")
    pin: str = Field(description="PIN Requester")
    ip: str = Field(description="IP address Requester")
    report_url: str | None = Field(
        ...,
        description="URL untuk laporan, jika Kosong akan di kembalikan ke IP Requester",
    )
    allow_no_sign: bool = Field(description="Izinkan request tanpa signature")

    @field_validator("pin", mode="before")
    def pin_to_str(cls, v):
        return str(v) if v is not None else ""


class MemberRequestWithSignature(BaseModel):
    memberid: str
    product: str
    signature: str


class MemberRequestWithoutSignature(BaseModel):
    memberid: str
    product: str
    pin: str
    password: str


# NOTE: nanti beresin masalah validasi dan lain lain sekarang focus dulu ke signature dan validasi request.
