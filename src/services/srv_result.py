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
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
        self.value = arg

    def __str__(self):
        return "[Success]" if self.success else f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        return (
            "<ServiceResult Success>"
            if self.success
            else f"<ServiceResult AppException {self.exception_case}>"
        )

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        # Tambahkan cleanup jika perlu (opsional)
        pass

    @property
    def data(self):
        """Akses langsung data jika success, kalau tidak akan None."""
        return self.value if self.success else None


def caller_info() -> str:
    """Ambil informasi lokasi pemanggil (debug helper)."""
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult, log_success: bool = False):
    """Eksekusi hasil service.

    - Jika gagal: log dan raise exception
    - Jika sukses: return result.value
    """
    if not result.success:
        with result as exception:
            logger.error(f"[Service Error] {exception} at {caller_info()}")
            raise exception
    else:
        if log_success:
            logger.info(f"[Service OK] from {caller_info()}")
        with result as result_value:
            return result_value
