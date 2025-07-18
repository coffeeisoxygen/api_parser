"""schemas for member."""

from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field, IPvAnyAddress, field_validator

# convert input integer ke string
StrFromInt = Annotated[
    str, BeforeValidator(lambda v: str(v) if isinstance(v, int) else v)
]

# convert ipaddress to Str Again after validation


class Member(BaseModel):
    model_config = {"str_strip_whitespace": True, "extra": "forbid"}
    memberid: str = Field(..., description="ID unik anggota")
    password: str = Field(..., description="Kata sandi anggota")
    pin: StrFromInt = Field(..., description="PIN anggota")
    ip: IPvAnyAddress = Field(..., description="Alamat IP anggota")
    report_url: str | None = Field(None, description="URL laporan anggota")
    allow_no_sign: bool = Field(
        False, description="Apakah transaksi tanpa tanda tangan diizinkan"
    )
    is_active: bool = Field(default=True, description="Status aktif anggota")

    @field_validator("pin", "password", mode="before")
    @classmethod
    def int_to_str(cls, v):
        if isinstance(v, int):
            return str(v)
        return v

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Pastikan ip dikonversi ke string
        data["ip"] = str(self.ip)
        return data
