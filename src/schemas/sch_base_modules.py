"""base Schemas buat modules tipe data."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class Module(BaseModel):
    """Schema dasar untuk modul OtomaX."""

    model_config = {
        "from_attributes": True,
        "str_strip_whitespace": True,
        "extra": "allow",
    }

    name: str = Field(..., description="Nama modul (ex: Digipos)")
    code: str = Field(..., description="Kode unik modul (ex: DIGIPOS)")
    description: str | None = Field(..., description="Deskripsi singkat tentang modul")
    base_url: str = Field(..., description="Base URL untuk modul (ex: http://...)")
    timeout: int = Field(5, description="Timeout dalam detik (default 5)")
    method: Literal["GET", "POST"] = Field(..., description="HTTP method untuk request")
    retry: int = Field(3, description="Jumlah percobaan ulang saat gagal")
    wait_seconds: int = Field(
        60, description="Waktu tunggu sebelum mencoba ulang dalam detik"
    )
    is_active: bool = Field(True, description="Apakah modul aktif atau tidak")
    parameters: dict[str, Any] | None = Field(
        None, description="Parameter khusus modul, opsional"
    )


# NOTE: field validator dan model validator nanti aja nyusul ya, semntara karena pake yaml , jadi belum perlu , tapi yg mandatory mah getter
