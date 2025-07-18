from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response

from src.exceptions.app_exceptions import AppExceptionError, app_exception_handler
from src.exceptions.oto_exceptions import OtoException, OtoExceptionError


async def global_exception_handler(request: Request, exc: Exception) -> Response:  # noqa: D103, RUF029
    if isinstance(exc, OtoExceptionError):
        return exc.render()

    elif isinstance(exc, AppExceptionError):
        return app_exception_handler(exc)

    elif isinstance(exc, RequestValidationError):
        # Ambil pesan pertama biar singkat
        first_error = exc.errors()[0]
        loc = ".".join(str(x) for x in first_error["loc"])
        msg = f"{loc}: {first_error['msg']}"
        return OtoException.InvalidTrxCombinationError(msg).render()

    return Response(status_code=500, content="Internal Server Error")
