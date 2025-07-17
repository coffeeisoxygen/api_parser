"""Advanced Loguru Logging (DI-style with LogConfig).

USAGE EXAMPLES:

Manual setup:
    from src.utils.mylogger import setup_logging, patch_uvicorn_loggers, LogConfig
    setup_logging(LogConfig(level="INFO", to_terminal=True, to_file=False, name_prefix="addon"))
    patch_uvicorn_loggers()

Auto inject from .env/settings:
    from src.config.settings import settings
    setup_logging(LogConfig(
        level=settings.app_log_level.upper(),
        to_terminal=True,
        to_file=settings.app_log_to_file,
        name_prefix=settings.app_mode,
    ))

Per-function usage:
    from src.utils.mylogger import logger, logger_wraps, timer, LogContext

    @logger_wraps(level="INFO")
    def myfunc(x):
        return x * 2

    @timer("my_operation")
    def slow_func():
        time.sleep(1)
        return "done"

    def run():
        with LogContext("my_block", level="INFO"):
            logger.info("Inside context block")
"""

# === CONFIG ===
import datetime
import functools
import inspect
import logging
import os
import sys
import time
import traceback
import types
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

from loguru import logger as loguru_logger


# === CONFIG ===
@dataclass
class LogConfig:
    level: str = "DEBUG"
    to_terminal: bool = True
    to_file: bool = False
    serialize: bool = False
    diagnose: bool = False
    enqueue: bool = True
    log_path: str = "logs"
    name_prefix: str = "app"
    size_mb: int = 10
    retention_days: int = 7


# === ROTATOR ===
class Rotator:
    def __init__(self, size: int, at: datetime.time):
        self._size_limit = size
        now = datetime.datetime.now()
        self._time_limit = now.replace(hour=at.hour, minute=at.minute, second=at.second)
        if now >= self._time_limit:
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message: Any, file: IO) -> bool:
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        if message.record["time"].timestamp() >= self._time_limit.timestamp():
            self._time_limit += datetime.timedelta(days=1)
            return True
        return False


# === OPENER ===
def opener(file: str, flags: int) -> int:
    return os.open(file, flags, 0o600)


# === FORMAT ===
loguru_logger.level("INFO", color="<cyan>")
loguru_logger.level("WARNING", color="<yellow>")
loguru_logger.level("ERROR", color="<red>")
loguru_logger.level("DEBUG", color="<blue>")
loguru_logger.level("TRACE", color="<white>")

FORMAT_STR = (
    "<level>{level: <8}</level> {time:YYYY-MM-DD HH:mm:ss} | "
    "<cyan>{process.name}:{thread.name}</cyan> | "
    "<magenta>{name}:{function}:{line}</magenta> | "
    "<level>{message}</level>"
)


# === MAIN SETUP ===
def setup_logging(config: LogConfig):
    r"""Setup loguru logging based on LogConfig.

    Example:
        setup_logging(LogConfig(level="INFO"))
    """
    loguru_logger.remove()
    Path(config.log_path).mkdir(parents=True, exist_ok=True)

    if config.to_terminal:
        loguru_logger.add(
            sys.stderr,
            level=config.level.upper(),
            format=FORMAT_STR,
            colorize=True,
            backtrace=True,
            diagnose=config.diagnose,
            enqueue=config.enqueue,
            serialize=config.serialize,
        )

    if config.to_file:
        rotator = Rotator(size=config.size_mb * 1_000_000, at=datetime.time(0, 0))

        loguru_logger.add(
            sink=f"{config.log_path}/{config.name_prefix}_app.log",
            level="INFO",
            format=FORMAT_STR,
            serialize=config.serialize,
            diagnose=config.diagnose,
            backtrace=True,
            enqueue=config.enqueue,
            rotation=rotator.should_rotate,
            retention=f"{config.retention_days} days",
            opener=opener,
        )

        loguru_logger.add(
            sink=f"{config.log_path}/{config.name_prefix}_error.log",
            level="ERROR",
            format=FORMAT_STR,
            serialize=config.serialize,
            diagnose=config.diagnose,
            backtrace=True,
            enqueue=config.enqueue,
            rotation=rotator.should_rotate,
            retention=f"{config.retention_days} days",
            opener=opener,
        )

    # Hijack stdlib logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: Any):
            try:
                levelname = loguru_logger.level(record.levelname).name
            except Exception:
                levelname = record.levelno
            frame, depth = inspect.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                levelname, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    loguru_logger.info("Logging initialized")


# === PATCH UVICORN ===
def patch_uvicorn_loggers():
    r"""Patch uvicorn loggers to use loguru for consistent logging output."""

    class Intercept(logging.Handler):
        def emit(self, record: Any):
            try:
                level = loguru_logger.level(record.levelname).name
            except Exception:
                level = record.levelno
            frame, depth = inspect.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).handlers = [Intercept()]
        logging.getLogger(name).propagate = False


# === UTILS ===
def logger_wraps(*, entry: bool = True, exit: bool = True, level: str = "DEBUG"):
    r"""Decorator to log function entry and exit with arguments and result.

    Example:
        @logger_wraps(level="INFO")
        def myfunc(x):
            return x * 2
    """

    def wrapper(func: Any):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if entry:
                loguru_logger.log(
                    level, f"→ {func.__name__} | args={args}, kwargs={kwargs}"
                )
            result = func(*args, **kwargs)
            if exit:
                loguru_logger.log(level, f"← {func.__name__} | result={result}")
            return result

        return wrapped

    return wrapper


def timer(operation: str | None = None):
    r"""Decorator to log execution time of a function.

    Example:
        @timer("my_operation")
        def slow_func():
            time.sleep(1)
            return "done"
    """

    def decorator(func: Any):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op = operation or func.__name__
            start = time.perf_counter()
            try:
                loguru_logger.info(f"[{op}] Starting...")
                result = func(*args, **kwargs)
                loguru_logger.info(
                    f"[{op}] Completed in {time.perf_counter() - start:.3f}s"
                )
            except Exception as e:
                loguru_logger.error(f"[{op}] Failed: {e}")
                raise
            return result

        return wrapper

    return decorator


class LogContext:
    r"""Context manager to log start, end, and error of a code block.

    Example:
        with LogContext("my_block", level="INFO"):
            logger.info("Inside context block")
    """

    def __init__(self, operation: str, level: str = "INFO"):
        self.operation = operation
        self.level = level
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        loguru_logger.log(self.level, f"[{self.operation}] Starting...")
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: types.TracebackType | None,
    ):
        duration = (
            time.perf_counter() - self.start_time if self.start_time else float("nan")
        )
        if exc_type:
            loguru_logger.error(
                f"[{self.operation}] Failed after {duration:.3f}s: {exc_val}"
            )
        else:
            loguru_logger.log(self.level, f"[{self.operation}] Done in {duration:.3f}s")


def log_with_stacktrace(message: str, level: str = "DEBUG"):
    r"""Log a message with the current stacktrace for debugging purposes.

    Example:
        log_with_stacktrace("Something happened", level="ERROR")
    """
    stack = "".join(traceback.format_stack())
    loguru_logger.log(level, f"{message}\nStacktrace:\n{stack}")


# === EXPORTS ===
logger = loguru_logger

__all__ = [
    "LogConfig",
    "LogContext",
    "Rotator",
    "log_with_stacktrace",
    "logger",
    "logger_wraps",
    "patch_uvicorn_loggers",
    "setup_logging",
    "timer",
]
