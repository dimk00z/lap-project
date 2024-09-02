import os
from dataclasses import dataclass, field

from litestar.data_extractors import RequestExtractorField, ResponseExtractorField


@dataclass
class LogSettings:
    """Logger configuration"""

    # https://stackoverflow.com/a/1845097/6560549
    EXCLUDE_PATHS: str = r"\A(?!x)x"
    """Regex to exclude paths from logging."""
    HTTP_EVENT: str = "HTTP"
    """Log event name for logs from Litestar handlers."""
    INCLUDE_COMPRESSED_BODY: bool = False
    """Include 'body' of compressed responses in log output."""
    LEVEL: int = field(
        default_factory=lambda: int(
            os.getenv("LOG_LEVEL", "10"),
        ),
    )
    """Stdlib log levels.

    Only emit logs at this level, or higher.
    """
    OBFUSCATE_COOKIES: set[str] = field(
        default_factory=lambda: {"session"},
    )
    """Request cookie keys to obfuscate."""
    OBFUSCATE_HEADERS: set[str] = field(
        default_factory=lambda: {"Authorization", "X-API-KEY"}
    )
    """Request header keys to obfuscate."""
    JOB_FIELDS: list[str] = field(
        default_factory=lambda: [
            "function",
            "kwargs",
            "key",
            "scheduled",
            "attempts",
            "completed",
            "queued",
            "started",
            "result",
            "error",
        ],
    )
    """Attributes of the SAQ.

    [`Job`](https://github.com/tobymao/saq/blob/master/saq/job.py) to be
    logged.
    """
    REQUEST_FIELDS: list[RequestExtractorField] = field(
        default_factory=lambda: [
            "path",
            "method",
            "headers",
            "cookies",
            "query",
            "path_params",
            "body",
        ],
    )
    """Attributes of the [Request][litestar.connection.request.Request] to be
    logged."""
    RESPONSE_FIELDS: list[ResponseExtractorField] = field(
        default_factory=lambda: [
            "status_code",
            "cookies",
            "headers",
            "body",
        ],
    )
    """Attributes of the [Response][litestar.response.Response] to be
    logged."""
    WORKER_EVENT: str = "Worker"
    """Log event name for logs from SAQ worker."""
    SAQ_LEVEL: int = 20
    """Level to log SAQ logs."""
    SQLALCHEMY_LEVEL: int = 20
    """Level to log SQLAlchemy logs."""
    UVICORN_ACCESS_LEVEL: int = 20
    """Level to log uvicorn access logs."""
    UVICORN_ERROR_LEVEL: int = 20
    """Level to log uvicorn error logs."""
    GRANIAN_ACCESS_LEVEL: int = 30
    """Level to log uvicorn access logs."""
    GRANIAN_ERROR_LEVEL: int = 20
    """Level to log uvicorn error logs."""
