"""schemas untuk model transaksi otomax ke middleware."""

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    """Schema dasar transaksi OtomaX."""

    model_config = {
        "from_attributes": True,
        "str_strip_whitespace": True,
        "extra": "forbid",
    }

    memberid: str = Field(..., alias="memberID", description="ID member / requester")
    product: str = Field(..., description="Produk yang diminta")
    dest: str = Field(..., description="Tujuan transaksi")
    refid: str = Field(..., alias="refID", description="Referensi ID transaksi")
    qty: int | None = Field(1, description="Jumlah transaksi, default 1")


class TransactionWithSignature(TransactionBase):
    signature: str = Field(..., description="Signature member untuk otentikasi")


class TransactionWithoutSignature(TransactionBase):
    pin: str = Field(..., description="PIN member")
    password: str = Field(..., description="Password member")
