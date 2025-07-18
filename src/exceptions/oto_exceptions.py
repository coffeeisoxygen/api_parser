from starlette.responses import PlainTextResponse

from src.exceptions.app_exceptions import AppExceptionError


class OtoExceptionError(AppExceptionError):
    """Base class untuk exception OtomaX, tapi response-nya plain text."""

    def render(self):
        """Custom render untuk FastAPI exception handler OtomaX."""
        status = getattr(self, "oto_status", 91)  # default unknown error
        message = self.context.get("message") or self.__class__.__name__
        dest = self.context.get("dest", "")
        refid = self.context.get("refid", "")
        return PlainTextResponse(
            content=f"status={status}&message={message}&dest={dest}&refid={refid}",
            status_code=self.status_code,
        )


class OtoException:
    """Namespace untuk exception OtomaX."""

    class ModuleNotFoundError(OtoExceptionError):
        """Exception ketika modul tidak ditemukan."""

        def __init__(self, code: str):
            super().__init__(status_code=404, context={"code": code})
            self.oto_status = 404
            self.context["message"] = f"Modul dengan kode '{code}' tidak ditemukan."
