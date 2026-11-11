"""Structured JSON logging with request/trace context propagation."""

from __future__ import annotations

import contextvars
import json
import logging
import sys
import traceback
from datetime import datetime, timezone
from typing import Any, Mapping


_log_context: contextvars.ContextVar[dict[str, Any]] = contextvars.ContextVar(
    "knowmesh_log_context", default={}
)


def bind_log_context(**values: Any):
    """Bind fields to log records in the current async/task context."""
    merged = dict(_log_context.get())
    merged.update(values)
    return _log_context.set(merged)


def clear_log_context() -> None:
    _log_context.set({})


class JsonFormatter(logging.Formatter):
    """Emit one JSON object per log event.

    Arbitrary objects are converted to strings. Sensitive fields should be
    filtered before they are passed as `extra` or context.
    """
    _standard = set(logging.makeLogRecord({}).__dict__) | {
        "message", "asctime", "taskName"
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        payload.update(_log_context.get())
        for key, value in record.__dict__.items():
            if key not in self._standard and not key.startswith("_"):
                payload[key] = value
        if record.exc_info:
            payload["exception"] = "".join(traceback.format_exception(*record.exc_info)).rstrip()
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)


class ContextLogger:
    """Small convenience wrapper around a standard logger."""
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def log(self, level: int, message: str, **fields: Any) -> None:
        self.logger.log(level, message, extra=fields)

    def debug(self, message: str, **fields: Any) -> None:
        self.log(logging.DEBUG, message, **fields)

    def info(self, message: str, **fields: Any) -> None:
        self.log(logging.INFO, message, **fields)

    def warning(self, message: str, **fields: Any) -> None:
        self.log(logging.WARNING, message, **fields)

    def error(self, message: str, **fields: Any) -> None:
        self.log(logging.ERROR, message, **fields)

    def exception(self, message: str, **fields: Any) -> None:
        self.logger.exception(message, extra=fields)


def configure_logging(*, level: int | str = logging.INFO,
                      stream=None, logger_name: str | None = None,
                      replace_handlers: bool = True) -> logging.Logger:
    """Configure JSON logging; idempotent when called repeatedly."""
    logger = logging.getLogger(logger_name)
    if isinstance(level, str):
        resolved = logging.getLevelName(level.upper())
        if not isinstance(resolved, int):
            raise ValueError(f"unknown log level: {level}")
        level = resolved
    logger.setLevel(level)
    logger.propagate = False
    if replace_handlers:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()
    if not logger.handlers:
        handler = logging.StreamHandler(stream or sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger


def get_logger(name: str) -> ContextLogger:
    return ContextLogger(logging.getLogger(name))
