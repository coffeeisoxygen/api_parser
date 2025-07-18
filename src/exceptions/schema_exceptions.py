"""Exception ringan khusus schema validation (digunakan di @validator).

✍️ Exception untuk validasi Pydantic
🚫 Tidak di-handle sendiri (biar FastAPI balikin 422)
✅ Raised di @field_validator, bukan service
Raise ValueError subclass agar dikenali Pydantic.
"""


class SchemaValidationError(ValueError):
    """Base class error validasi Pydantic (akan ditangkap FastAPI jadi 422)."""

    def __init__(self, message: str):
        super().__init__(message)


class PasswordTooWeakError(SchemaValidationError):
    def __init__(self):
        super().__init__(
            "Password terlalu lemah (minimal 6 karakter + kombinasi angka huruf)"
        )


class PinInvalidFormatError(SchemaValidationError):
    def __init__(self):
        super().__init__("Format PIN harus 4 digit angka (contoh: 1234)")
