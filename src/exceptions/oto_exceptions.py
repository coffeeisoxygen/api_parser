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

        for k in ("dest", "refid"):
            if k in self.context:
                parts.append(f"{k}={self.context[k]}")

        return PlainTextResponse(content="&".join(parts), status_code=self.status_code)


class OtoException:
    class ModuleNotFound(OtoExceptionError):
        def __init__(self, code: str):
            super().__init__(404, {"code": code})
            self.oto_status = 404
            self.context["message"] = f"Module '{code}' tidak ditemukan"

    class InvalidTrxCombination(OtoExceptionError):
        def __init__(self, message: str):
            super().__init__(422, {"message": message})
            self.oto_status = 422
