from typing import Any

from pydantic import BaseModel, Field


class ProductModuleMapping(BaseModel):
    product_code: str = Field(..., description="Kode produk")
    module_code: str = Field(..., description="Kode modul")
    command: str = Field(..., description="Nama command")
    query_params: dict[str, Any] = Field(
        ..., description="Parameter query fleksibel untuk command"
    )
    is_active: bool = Field(..., description="Status aktif mapping")


class ProductModuleMappingList(BaseModel):
    product_module_mapping: list[ProductModuleMapping] = Field(
        ..., description="Daftar mapping produk ke modul"
    )


# NOTE: field validator dan model validator nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
