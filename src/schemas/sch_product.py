"""schemas crud untuk product."""

from pydantic import BaseModel, Field


class Product(BaseModel):
    model_config = {"str_strip_whitespace": True, "extra": "forbid"}
    code: str = Field(..., description="Kode produk unik")
    name: str = Field(..., description="Nama produk")
    provider: str = Field(..., description="Nama provider (ex: TELKOMSEL)")
    is_active: bool = Field(default=True, description="Apakah produk aktif")


# NOTE : field validator dan model validator nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
