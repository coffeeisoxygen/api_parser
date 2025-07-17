from typing import Literal

from pydantic import BaseModel, Field


class Product(BaseModel):
    code: str = Field(..., description="Kode produk unik")
    name: str = Field(..., description="Nama produk")
    provider: str = Field(..., description="Nama provider (ex: TELKOMSEL)")
    command: str = Field(..., description="Perintah query yang akan di-forward")


class Module(BaseModel):
    name: str = Field(..., description="Nama modul (ex: Digipos)")
    code: str = Field(..., description="Kode unik modul (ex: DIGIPOS)")
    base_url: str = Field(..., description="Base URL untuk modul (ex: http://...)")
    timeout: int = Field(5, description="Timeout dalam detik (default 5)")
    methode: Literal["GET", "POST"] = Field(
        ..., description="HTTP method untuk request"
    )
    retry: int = Field(3, description="Jumlah percobaan ulang saat gagal")
    products: list[Product] = Field(..., description="List produk dalam modul")


class ModuleList(BaseModel):
    modules: list[Module] = Field(..., description="Daftar semua modul yang tersedia")
