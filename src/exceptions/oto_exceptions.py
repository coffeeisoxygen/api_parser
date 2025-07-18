"""Exception khusus untuk OtomaX client. Response plain-text (bukan JSON).

🔃 Untuk client OtomaX
📄 Respon plain/text dengan format: status=..&message=...&dest=...&refid=...
🧩 Dipakai di route OtomaX (/trx, /report, dll)
Format: status=..&message=..&[dest=..&refid=..]
"""

from starlette.responses import PlainTextResponse

from src.exceptions.app_exceptions import AppExceptionError


class OtoExceptionError(AppExceptionError):
    def render(self):
        status = getattr(self, "oto_status", 91)
        message = self.context.get("message") or self.__class__.__name__
        parts = [f"status={status}", f"message={message}"]

        parts.extend(
            f"{k}={self.context[k]}" for k in ("dest", "refid") if k in self.context
        )

        return PlainTextResponse(content="&".join(parts), status_code=self.status_code)


class OtoException:
    class ModuleNotFoundError(OtoExceptionError):
        """Exception yang di-raise ketika modul tidak ditemukan.

        Exception ini digunakan untuk menandai bahwa modul yang diminta
        tidak dapat ditemukan dalam sistem.

        Args:
            OtoExceptionError (_type_): Kelas dasar untuk exception OtomaX.
        """

        def __init__(self, code: str):
            super().__init__(404, {"code": code})
            self.oto_status = 404
            self.context["message"] = f"Module '{code}' tidak ditemukan"

    class ModuleIsInActiveError(OtoExceptionError):
        """Exception yang di-raise ketika modul tidak aktif.

        Exception ini digunakan untuk menandai bahwa modul yang diminta
        tidak aktif dan tidak dapat digunakan.

        Args:
            OtoExceptionError (_type_): Kelas dasar untuk exception OtomaX.
        """

        def __init__(self, code: str):
            super().__init__(404, {"code": code})
            self.oto_status = 404
            self.context["message"] = f"Module '{code}' tidak ditemukan"

    class InvalidTrxCombinationError(OtoExceptionError):
        """Exception yang di-raise ketika kombinasi transaksi tidak valid."""

        def __init__(self, message: str):
            super().__init__(422, {"message": message})
            self.oto_status = 422
            self.context["message"] = message

    class UnknownModuleValidationError(OtoExceptionError):
        """Exception untuk error validasi modul yang tidak diketahui."""

        def __init__(self, code: str | None = None):
            super().__init__(500, {"code": code})
            self.oto_status = 500
            self.context["message"] = "Unknown module validation error"
