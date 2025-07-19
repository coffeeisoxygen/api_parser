# src/services/accept_response.py

from httpx import Response

from src.utils.mylogger import logger


class ResponseHandler:
    @staticmethod
    def parse(response: Response | None) -> str | dict:
        if not response:
            return "ERROR: Tidak ada response dari target"

        content_type = response.headers.get("Content-Type", "")
        logger.debug(f"[RESPONSE] Content-Type: {content_type}")
        logger.debug(f"[RESPONSE] Status: {response.status_code}")

        # Coba parse json
        if "application/json" in content_type:
            try:
                json_data = response.json()
                logger.debug(f"[RESPONSE] JSON Preview: {str(json_data)[:500]}")
                return json_data
            except Exception as e:
                logger.warning(f"[RESPONSE] Gagal parse JSON: {e}")

        # Fallback ke text
        logger.debug(f"[RESPONSE] Text Preview: {response.text[:500]}")
        return response.text
