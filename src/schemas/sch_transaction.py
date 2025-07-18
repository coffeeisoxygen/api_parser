"""schemas untuk model transaksi otomax ke middleware."""

from pydantic import BaseModel, Field


class TrxRequestQuery(BaseModel):
    product: str = Field(..., description="Kode produk")
    dest: str = Field(..., description="Nomor tujuan")
    refid: str = Field(..., description="ID referensi transaksi")
    memberid: str = Field(..., description="ID member")
    sign: str | None = Field(None, description="Signature (opsional)")
    pin: str | None = Field(None, description="PIN member (opsional)")
    pass_: str | None = Field(
        None, alias="pass", description="Password member (opsional)"
    )
    qty: int = Field(default=1, description="Jumlah produk")
