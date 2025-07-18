from starlette.responses import PlainTextResponse

from src.exceptions.app_exceptions import AppExceptionError


class OtoExceptionError(AppExceptionError):
    """Base class untuk exception OtomaX, tapi response-nya plain text."""

    def render(self):
        """Custom render untuk FastAPI exception handler OtomaX."""
        status = getattr(self, "oto_status", 91)  # default unknown error
        message = self.context.get("message") or self.__class__.__name__
        # Hanya tampilkan dest/refid jika ada di context
        parts = [f"status={status}", f"message={message}"]
        if "dest" in self.context:
            parts.append(f"dest={self.context['dest']}")
        if "refid" in self.context:
            parts.append(f"refid={self.context['refid']}")
        return PlainTextResponse(content="&".join(parts), status_code=self.status_code)


class OtoException:
    """Namespace untuk exception OtomaX."""

    class ModuleNotFoundError(OtoExceptionError):
        """Exception ketika modul tidak ditemukan."""

        def __init__(self, code: str):
            super().__init__(status_code=404, context={"code": code})
            self.oto_status = 404
            self.context["message"] = f"Modul dengan kode '{code}' tidak ditemukan."

        def render(self):
            return PlainTextResponse(
                content=f"status={self.oto_status}&message={self.context['message']}",
                status_code=self.status_code,
            )

    class InvalidTrxCombinationError(OtoExceptionError):
        """Exception untuk kombinasi field transaksi yang tidak valid (pin/pass/sign)."""

        def __init__(self, message: str):
            super().__init__(status_code=422, context={"message": message})
            self.oto_status = 422

        def render(self):
            return PlainTextResponse(
                content=f"status={self.oto_status}&message={self.context['message']}",
                status_code=self.status_code,
            )
