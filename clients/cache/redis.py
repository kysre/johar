import os
from redis import Redis


class RedisConfig:
    def __init__(self):
        self.host: str = os.getenv("REDIS_HOST", "localhost")
        self.port: int = int(os.getenv("REDIS_PORT", 6379))
        self.password: str = os.getenv("REDIS_PASSWORD", "")
        self.socket_timeout: float = float(os.getenv("REDIS_SOCKET_TIMEOUT", 3.0))
        self.socket_connect_timeout: float = float(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT", 3.0))
        self.socket_keepalive: bool = os.getenv("REDIS_SOCKET_KEEPALIVE", "True").lower() == "true"
        self.retry_on_timeout: bool = os.getenv("REDIS_RETRY_ON_TIMEOUT", "False").lower() == "true"


def create_redis_client(config: RedisConfig = None) -> Redis:
    if config is None:
        config = RedisConfig()
        config.db = int(os.getenv("REDIS_DB", 0))
    client = Redis(
        host=config.host,
        port=config.port,
        db=config.db,
        password=config.password,
        socket_timeout=config.socket_timeout,
        socket_connect_timeout=config.socket_connect_timeout,
        socket_keepalive=config.socket_keepalive,
        retry_on_timeout=config.retry_on_timeout
    )
    return client
