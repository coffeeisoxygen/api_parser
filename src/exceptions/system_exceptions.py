"""Exception fatal yg menyebabkan app tidak bisa jalan (stop FastAPI).

Tidak ditangani custom handler.
❗FATAL error → bikin aplikasi stop jalan
❌ Tidak ditangani FastAPI handler
🛠 Digunakan di level startup / config / repo init
"""


class ModelNotSetError(RuntimeError):
    """BaseYamlRepo: model belum di-set di subclass (harus manual per repo)."""

    def __init__(self):
        super().__init__("BaseYamlRepo: 'model' attribute must be set in subclass.")


class RegistryFileNotFoundError(FileNotFoundError):
    """File registry tidak ditemukan saat startup (YAML wajib ada)."""

    def __init__(self, name: str, path: str):
        super().__init__(f"File registry '{name}' tidak ditemukan: {path}")
