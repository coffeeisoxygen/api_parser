"""service memantau file YAML dan reload otomatis jika file diubah."""

import asyncio
import threading
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.exceptions.app_exceptions import AppException
from src.utils.mylogger import logger


class YamlReloadHandler(FileSystemEventHandler):
    def __init__(self, repo, loop: asyncio.AbstractEventLoop):  # noqa: ANN001
        self.repo = repo
        self.loop = loop
        self.file_path = str(repo.file_path.resolve())

    def on_modified(self, event):  # noqa: ANN001
        # Normalisasi dulu kedua path ke Path.resolve()
        src_path = event.src_path
        if isinstance(src_path, bytes):
            src_path = src_path.decode()  # Pastikan str
        event_path = Path(src_path).resolve()
        target_path = Path(self.file_path).resolve()

        if not event.is_directory and event_path == target_path:
            logger.info(f"[YAML Watch] Perubahan terdeteksi: {event_path}")
            asyncio.run_coroutine_threadsafe(self._safe_reload(), self.loop)

    async def _safe_reload(self):
        try:
            new_items = await self.repo._load_items()
            self.repo._items.clear()  # kosongin dulu
            self.repo._items.extend(new_items)  # masukin item baru yg valid
            self.repo.last_loaded_at = datetime.now()
            self.repo.invalid_count = 0
            logger.success(f"[YAML Watch] Reload sukses: {self.file_path}")
        except Exception as e:
            self.repo.invalid_count += 1  # atau simpan detail error
            logger.warning(f"[YAML Watch] Reload gagal: {e} → pakai data lama")


def watch_yaml_repo(repo):  # noqa: ANN001
    """Aktifkan file watcher untuk satu repo berbasis file YAML."""
    if not hasattr(repo, "file_path"):
        raise AppException.RepoFilePathMissingError()

    loop = asyncio.get_event_loop()
    handler = YamlReloadHandler(repo, loop)
    observer = Observer()
    observer.schedule(handler, str(Path(repo.file_path).parent), recursive=False)

    thread = threading.Thread(target=observer.start, daemon=True)
    thread.start()
    logger.info(f"[YAML Watch] Watcher aktif untuk: {repo.file_path}")
