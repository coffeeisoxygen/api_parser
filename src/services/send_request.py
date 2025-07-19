# src/services/send_request.py

import asyncio

import httpx

from src.schemas.sch_module import Module
from src.utils.mylogger import logger


class RequestForwarder:
    def __init__(self, module: Module):
        self.module = module
        self.method = (module.method or "GET").upper()
        self.timeout = module.timeout or 10
        self.retry = module.retry or 1
        self.wait = module.wait_seconds or 0

    async def send(self, url: str) -> httpx.Response | None:
        logger.info(f"[FORWARD] Mulai request: {self.method} {url}")
        logger.debug(
            f"[FORWARD] Config → timeout={self.timeout}s, retry={self.retry}, wait={self.wait}s"
        )

        for attempt in range(1, self.retry + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    if self.method == "GET":
                        response = await client.get(url)
                    elif self.method == "POST":
                        response = await client.post(url)
                    else:
                        raise ValueError(
                            f"[FORWARD] Method tidak didukung: {self.method}"
                        )

                logger.info(
                    f"[FORWARD] Berhasil [Attempt-{attempt}], status: {response.status_code}"
                )
                return response

            except httpx.RequestError as e:
                logger.warning(f"[FORWARD] Gagal [Attempt-{attempt}]: {e}")
                if attempt < self.retry and self.wait:
                    logger.info(f"[FORWARD] Tunggu {self.wait}s sebelum retry...")
                    await asyncio.sleep(self.wait)

        logger.error("[FORWARD] Semua attempt gagal. Tidak ada response dari target.")
        return None
