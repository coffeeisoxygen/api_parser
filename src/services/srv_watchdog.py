"""service memantau file."""

import asyncio
import threading
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.utils.mylogger import logger


class YamlReloadHandler(FileSystemEventHandler):
    def __init__(self, repo, loop: asyncio.AbstractEventLoop):
        self.repo = repo
        self.loop = loop
        self.file_path = str(repo.file_path.resolve())

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.file_path:
            logger.info(f"[YAML Watch] Perubahan terdeteksi: {event.src_path}")
            asyncio.run_coroutine_threadsafe(self._safe_reload(), self.loop)

    async def _safe_reload(self):
        try:
            new_items = await self.repo._load_items()
            self.repo._items = new_items
            logger.success(f"[YAML Watch] Reload sukses: {self.file_path}")
        except Exception:
            logger.warning("[YAML Watch] Reload gagal, tetap pakai data lama")


def watch_yaml_repo(repo):
    """Aktifkan watcher untuk satu repo berbasis file YAML."""
    if not hasattr(repo, "file_path"):
        raise ValueError("Repo tidak punya file_path")

    loop = asyncio.get_event_loop()
    handler = YamlReloadHandler(repo, loop)
    observer = Observer()
    observer.schedule(handler, str(Path(repo.file_path).parent), recursive=False)

    thread = threading.Thread(target=observer.start, daemon=True)
    thread.start()
    logger.info(f"[YAML Watch] Watcher aktif untuk: {repo.file_path}")
