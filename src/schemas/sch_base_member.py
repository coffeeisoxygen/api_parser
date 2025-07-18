"""schemas untuk crud member, untuk sekarang kita akan melakukan nya dengan yaml."""

from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field, IPvAnyAddress

StrFromInt = Annotated[
    str, BeforeValidator(lambda v: str(v) if isinstance(v, int) else v)
]


class Member(BaseModel):
    model_config = {
        "from_attributes": True,
        "str_strip_whitespace": True,
        "extra": "forbid",  # strict: hanya field yang didefinisikan
    }
    memberid: str = Field(..., description="ID unik member")
    password: str = Field(..., description="Password member")
    pin: StrFromInt = Field(..., description="PIN member")
    ip: IPvAnyAddress = Field(..., description="IP address member")
    report_url: str | None = Field(None, description="URL untuk report, bisa null")
    allow_no_sign: bool = Field(..., description="Apakah diperbolehkan tanpa sign")
    is_active: bool = Field(default=True, description="Apakah member aktif")


PinToStr = Annotated[str, Field(..., description="PIN member")]
