# src/services/response_trimmer.py

from src.utils.mylogger import logger

class ResponseTrimmer:
    def __init__(self, field_key: str = "paket", prefix_key: str = "to", status_key: str = "status"):
        self.field_key = field_key
        self.prefix_key = prefix_key
        self.status_key = status_key

    def trim(self, response: dict) -> str:
        logger.debug("[TRIMMER] Mulai trimming response...")

        status = str(response.get(self.status_key, "success"))
        to = str(response.get(self.prefix_key, ""))
        items = response.get(self.field_key, [])

        if not isinstance(items, list):
            logger.warning("[TRIMMER] Field 'paket' bukan list")
            return f"status=failed&to={to}&message="

        messages = []
        for item in items:
            if not isinstance(item, dict):
                continue
            value_line = "-".join([str(v) for v in item.values()])
            messages.append(f"#{value_line}")

        result = f"status={status}&to={to}&message={''.join(messages)}"
        logger.info(f"[TRIMMER] Final trimmed: {result}")
        return result
