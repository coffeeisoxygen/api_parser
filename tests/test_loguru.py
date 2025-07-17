from loguru import logger


def test_loguru_integration(caplog):
    logger.debug("Hallo debug message")
    logger.info("Hallo info message")
    logger.error("Hallo error message")

    assert "Hallo info message" in caplog.text
    assert "Hallo error message" in caplog.text
    assert "Hallo debug message" in caplog.text
