"""semua transaksi wajib menggunakan signature."""

from pydantic import BaseModel


class TrxRequest(BaseModel):
    product: str
    dest: str
    refid: str
    memberid: str
    sign: str

    model_config = {"str_strip_whitespace": True, "extra": "forbid"}
