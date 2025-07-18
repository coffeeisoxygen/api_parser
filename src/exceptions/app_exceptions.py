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
    """Kumpulan exception logic internal (bukan fatal) untuk aplikasi.

    Semua exception di sini merupakan turunan dari AppExceptionError dan digunakan untuk
    error yang bisa di-handle di level service/route. Exception ini akan di-handle oleh
    handler khusus dan mengembalikan response JSON yang sesuai ke frontend/admin panel.

    Contoh error yang didefinisikan:
    - IPNotFoundError: IP client tidak terdaftar di registry member.
    - MemberNotFoundError: Member tidak ditemukan.
    - YamlFileNotFoundError: File YAML tidak ditemukan.
    - DuplicateItemError: Ada item duplikat pada registry/data.

    Exception ini aman untuk ditampilkan/log di frontend/admin.
    """

    class IPNotFoundError(AppExceptionError):
        """IP client tidak terdaftar di member registry."""

        def __init__(self, ip: str):
            super().__init__(
                HTTPStatus.NOT_FOUND, {"message": f"IP '{ip}' tidak ditemukan"}
            )

    class MemberNotFoundError(AppExceptionError):
        """Member tidak ditemukan berdasarkan ID."""

        def __init__(self, member_id: str):
            super().__init__(
                HTTPStatus.NOT_FOUND,
                {"message": f"Member '{member_id}' tidak ditemukan"},
            )

    class YamlFileNotFoundError(AppExceptionError):
        """YAML file tidak ditemukan."""

        def __init__(self, path: str):
            super().__init__(500, {"message": f"YAML file tidak ditemukan: {path}"})

    class DuplicateItemError(AppExceptionError):
        """Ada item duplikat pada registry/data."""

        def __init__(self, name: str, key: str):
            super().__init__(400, {"message": f"Duplicate {name}: {key}"})

    class ItemNotFoundError(AppExceptionError):
        """Item tidak ditemukan berdasarkan unique key."""

        def __init__(self, name: str, key: str):
            super().__init__(
                404, {"message": f"{name} dengan key '{key}' tidak ditemukan"}
            )
            self.unique_name = name
            self.unique_key = key

    class ModelNotSetError(AppExceptionError):
        """Model belum di-set di subclass BaseYamlRepo."""

        def __init__(self):
            super().__init__(
                500, {"message": "Model belum di-set di subclass BaseYamlRepo"}
            )

    class RepoFilePathMissingError(AppExceptionError):
        """Repo tidak punya file_path attribute."""

        def __init__(self):
            super().__init__(400, {"message": "Repo tidak punya file_path"})


def app_exception_handler(exc: AppExceptionError):
    """Handler untuk AppExceptionError, mengembalikan JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )
