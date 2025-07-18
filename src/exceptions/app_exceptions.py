"""exception ini tuh buat frontend nanti , klo jadi bikin admin panel + database."""

from http import HTTPStatus

from starlette.responses import JSONResponse


class AppExceptionError(Exception):
    """Base exception class for application-specific errors.

    Attributes:
        status_code (int): HTTP status code for the error.
        context (dict): Additional context for the error.
        exception_case (str): Name of the exception class.
    """

    def __init__(self, status_code: int, context: dict | None = None):
        """Initialize the exception with status code and context.

        Args:
            status_code (int): HTTP status code.
            context (dict, optional): Additional context for the error.
        """
        self.status_code = status_code
        self.context = context or {}

    @property
    def error(self):
        return self

    @property
    def exception_case(self):
        return self.__class__.__name__

    def __str__(self):
        """String representation of the exception.

        Returns:
            str: Formatted exception string.
        """
        return f"<AppException {self.exception_case}: {self.context}>"


# ✅ Optional handler (dipasang di FastAPI router)
def app_exception_handler(exc: AppExceptionError):
    """FastAPI exception handler for AppExceptionError.

    Args:
        exc (AppExceptionError): The exception instance.

    Returns:
        JSONResponse: Response with error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )


class AppException:
    """Namespace for application-specific exceptions."""

    class IPNotFoundError(AppExceptionError):
        """Exception raised when an IP address is not found."""

        def __init__(self, ip: str):
            super().__init__(
                status_code=HTTPStatus.NOT_FOUND,
                context={"message": f"IP address '{ip}' not found."},
            )
