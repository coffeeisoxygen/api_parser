from fastapi import Request
from fastapi.responses import Response

from src.exceptions.app_exceptions import AppExceptionError, app_exception_handler
from src.exceptions.oto_exceptions import OtoExceptionError


async def global_exception_handler(request: Request, exc: Exception) -> Response:  # noqa: D103, RUF029
    if isinstance(exc, OtoExceptionError):
        return exc.render()
    elif isinstance(exc, AppExceptionError):
        return app_exception_handler(exc)
    return Response(status_code=500, content="Internal Server Error")
