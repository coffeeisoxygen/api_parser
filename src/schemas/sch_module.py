from pydantic import BaseModel, Field


class ProductItem(BaseModel):
    code: str = Field(..., description="Kode unik untuk product")
    name: str = Field(..., description="Nama product (untuk manusia)")
    provider: str = Field(..., description="Nama provider, ex: TELKOMSEL")
    command: str = Field(..., description="Command yang akan dikirim ke target")


class ModuleItem(BaseModel):
    name: str = Field(..., description="Nama modul (ex: Digipos)")
    code: str = Field(..., description="Kode unik modul")
    base_url: str = Field(..., description="Base URL tujuan untuk forward")
    products: list[ProductItem] = Field(
        default_factory=list, description="List produk yang tersedia"
    )
