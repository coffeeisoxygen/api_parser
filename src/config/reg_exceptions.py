from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

from src.exceptions.app_exceptions import AppExceptionError, app_exception_handler
from src.exceptions.oto_exceptions import OtoExceptionError
from src.exceptions.repo_exceptions import ItemNotFoundError


def register_exception_handlers(app: FastAPI):
    """Daftarkan semua exception handler utama ke FastAPI app."""

    @app.exception_handler(OtoExceptionError)
    async def oto_exception_handler(request: Request, exc: OtoExceptionError):
        return exc.render()

    @app.exception_handler(AppExceptionError)
    async def app_exception_handler_fastapi(request: Request, exc: AppExceptionError):
        return app_exception_handler(exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        messages = []
        for err in exc.errors():
            loc = ".".join(str(l) for l in err["loc"])
            msg = err["msg"]
            messages.append(f"{loc}: {msg}")
        message = "; ".join(messages)
        return PlainTextResponse(
            content=f"status=422&message={message}", status_code=422
        )

    @app.exception_handler(ItemNotFoundError)
    async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
        return app_exception_handler(exc)
