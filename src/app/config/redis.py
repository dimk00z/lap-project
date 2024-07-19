import os
from dataclasses import dataclass, field

from redis.asyncio import Redis

from src.app.config.common import TRUE_VALUES


@dataclass
class RedisSettings:
    URL: str = field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )
    """A Redis connection URL."""
    SOCKET_CONNECT_TIMEOUT: int = field(
        default_factory=lambda: int(os.getenv("REDIS_CONNECT_TIMEOUT", "5"))
    )
    """Length of time to wait (in seconds) for a connection to become
    active."""
    HEALTH_CHECK_INTERVAL: int = field(
        default_factory=lambda: int(os.getenv("REDIS_HEALTH_CHECK_INTERVAL", "5"))
    )
    """Length of time to wait (in seconds) before testing connection health."""
    SOCKET_KEEPALIVE: bool = field(
        default_factory=lambda: os.getenv("REDIS_SOCKET_KEEPALIVE", "True")
        in TRUE_VALUES,
    )
    """Length of time to wait (in seconds) between keepalive commands."""
    _redis_instance: Redis | None = None
    """Redis instance generated from settings."""

    @property
    def client(self) -> Redis:
        return self.get_client()

    def get_client(self) -> Redis:
        if self._redis_instance is not None:
            return self._redis_instance
        self._redis_instance = Redis.from_url(
            url=self.URL,
            encoding="utf-8",
            decode_responses=False,
            socket_connect_timeout=self.SOCKET_CONNECT_TIMEOUT,
            socket_keepalive=self.SOCKET_KEEPALIVE,
            health_check_interval=self.HEALTH_CHECK_INTERVAL,
        )
        return self._redis_instance
