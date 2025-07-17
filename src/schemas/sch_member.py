"""schema untuk member yang akan consume API middleware."""

from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, Field


def convert_int_to_str(value: Any) -> str:
    """Mengubah nilai apapun menjadi string."""
    return str(value)


class Member(BaseModel):
    model_config = {
        "from_attributes": True,
        "str_strip_whitespace": True,
        "extra": "forbid",
    }

    memberid: str = Field(description="ID Requester")
    password: str = Field(description="Password Requester")
    pin: Annotated[str, BeforeValidator(convert_int_to_str)]
    ip: str = Field(description="IP address Requester")
    report_url: str | None = Field(
        ...,
        description="URL untuk laporan, jika Kosong akan di kembalikan ke IP Requester",
    )
    allow_no_sign: bool = Field(description="Izinkan request tanpa signature")


class RequestConfig(BaseModel):
    model_config = {"from_attributes": True, "extra": "allow"}


class MemberRequest(RequestConfig):
    memberid: str
    product: str
    dest: str
    refid: str


class MemberRequestWithSignature(MemberRequest):
    signature: str


class MemberRequestWithoutSignature(MemberRequest):
    pin: str
    password: str


# NOTE: nanti beresin masalah validasi dan lain lain sekarang focus dulu ke signature dan validasi request.
