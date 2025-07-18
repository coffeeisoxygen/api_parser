"""Exception logic internal (bukan fatal).

🧠 Logic-level error, aman, ditangani handler
🎯 Untuk route internal/admin (JSON response)
✅ Bisa log / ditampilkan di frontend (admin panel)
Dipakai di service layer, akan di-handle dan return JSON.
"""

from http import HTTPStatus

from starlette.responses import JSONResponse


class AppExceptionError(Exception):
    """Base class untuk semua error logic yang bisa di-handle."""

    def __init__(self, status_code: int, context: dict | None = None):
        self.status_code = status_code
        self.context = context or {}

    @property
    def exception_case(self):
        return self.__class__.__name__

    def __str__(self):
        return f"<AppException {self.exception_case}: {self.context}>"


class AppException:
    class IPNotFoundError(AppExceptionError):
        """IP client tidak terdaftar di member registry."""

        def __init__(self, ip: str):
            super().__init__(
                HTTPStatus.NOT_FOUND, {"message": f"IP '{ip}' tidak ditemukan"}
            )

    class MemberNotFoundError(AppExceptionError):
        def __init__(self, member_id: str):
            super().__init__(
                HTTPStatus.NOT_FOUND,
                {"message": f"Member '{member_id}' tidak ditemukan"},
            )

    class YamlFileNotFoundError(AppExceptionError):
        def __init__(self, path: str):
            super().__init__(500, {"message": f"YAML file tidak ditemukan: {path}"})

    class DuplicateItemError(AppExceptionError):
        def __init__(self, name: str, key: str):
            super().__init__(400, {"message": f"Duplicate {name}: {key}"})


def app_exception_handler(exc: AppExceptionError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )
