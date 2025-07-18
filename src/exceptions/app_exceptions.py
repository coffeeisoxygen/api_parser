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

    class MemberNotFoundError(AppExceptionError):
        """Exception raised when a member is not found."""

        def __init__(self, memberid: str):
            super().__init__(
                status_code=HTTPStatus.NOT_FOUND, context={"memberid": memberid}
            )

    class IPNotVerifiedError(AppExceptionError):
        """Exception raised when an IP is not verified."""

        def __init__(self, ip: str):
            super().__init__(status_code=HTTPStatus.UNAUTHORIZED, context={"ip": ip})

    class InvalidCredentialsError(AppExceptionError):
        """Exception raised for invalid credentials."""

        def __init__(self, memberid: str):
            super().__init__(
                status_code=HTTPStatus.UNAUTHORIZED, context={"memberid": memberid}
            )

    class ReportUrlNotFoundError(AppExceptionError):
        """Exception raised when report URL is not found for a member."""

        def __init__(self, memberid: str):
            super().__init__(
                status_code=HTTPStatus.NOT_FOUND,
                context={"memberid": memberid, "report_url": None},
            )

    class NoMembersFoundError(AppExceptionError):
        """Exception raised when no members are found in the repository."""

        def __init__(self):
            super().__init__(status_code=HTTPStatus.NOT_FOUND, context={"members": []})

    class SignatureRequiredError(AppExceptionError):
        """Exception raised when signature is required but not provided."""

        def __init__(self, memberid: str):
            super().__init__(
                status_code=HTTPStatus.FORBIDDEN,
                context={"memberid": memberid, "signature_required": True},
            )

    class InvalidSignatureError(AppExceptionError):
        """Exception raised for invalid signature."""

        def __init__(self, received_sign: str):
            super().__init__(
                status_code=HTTPStatus.UNAUTHORIZED,
                context={"message": "Invalid Signature", "received": received_sign},
            )

    class ModuleNotFoundError(AppExceptionError):
        """Exception raised when a module is not found."""

        def __init__(self, module_code: str):
            super().__init__(status_code=404, context={"module": module_code})

    class ProductNotFoundError(AppExceptionError):
        """Exception raised when a product is not found."""

        def __init__(self, product_code: str):
            super().__init__(status_code=404, context={"product": product_code})
