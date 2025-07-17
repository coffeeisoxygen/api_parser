"""module ini buat ngebungkus result.

Modul ini menangani hasil operasi service layer secara terstruktur dan konsisten.
Cocok digunakan untuk semua service di backend agar response error lebih clean dan predictable.

- Kelas `ServiceResult` membungkus hasil sukses atau gagal dari service.
- Fungsi `handle_result()` digunakan untuk mengeksekusi hasil tersebut:
  - Jika sukses: return value-nya
  - Jika gagal: raise exception sesuai `AppExceptionError` bawaan

Built with ❤️ by Hasan Maki and ChatGPT
"""

import inspect
from typing import Any

from src.exceptions.app_exceptions import AppExceptionError
from utils.mylogger import logger


class ServiceResult:
    def __init__(self, arg: Any):
        if isinstance(arg, AppExceptionError):
            self.success = False
            self.exception: AppExceptionError | None = arg
            self.value = None
        else:
            self.success = True
            self.value = arg
            self.exception: AppExceptionError | None = None

    @property
    def error(self):
        return self.exception if not self.success else None

    @property
    def data(self):
        """Akses langsung data jika success, None jika gagal."""
        return self.value if self.success else None

    def __str__(self):
        if self.success:
            return "[Success]"
        else:
            return f'[Exception] "{type(self.exception).__name__}: {self.exception}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        else:
            return f"<ServiceResult AppException {type(self.exception).__name__}>"

    def __enter__(self):
        return self.value if self.success else self.exception

    def __exit__(self, *kwargs) -> None:
        """Context manager support for ServiceResult."""
        pass


def caller_info() -> str:
    """Ambil informasi lokasi pemanggil (debug helper)."""
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


class NoServiceResultExceptionError(Exception):
    def __init__(self):
        super().__init__("ServiceResult contains no exception to raise")


def handle_result(result: ServiceResult, log_success: bool = False):
    """Eksekusi hasil service.

    - Jika gagal: log dan raise exception
    - Jika sukses: return result.value
    """
    if not result.success:
        with result as exception:
            logger.error(f"[Service Error] {exception} at {caller_info()}")
            if exception is not None:
                raise exception
            else:
                raise NoServiceResultExceptionError()
    else:
        if log_success:
            logger.info(f"[Service OK] from {caller_info()}")
        with result as result_value:
            return result_value
