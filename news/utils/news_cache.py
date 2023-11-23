import os
from clients.cache.redis import RedisConfig, create_redis_client

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


class NewsCache:
    _redis_client = None
    _landing_view_ttl = None
    _news_data_ttl = None

    @classmethod
    def _get_redis_connection(cls):
        redis_config = RedisConfig()
        redis_config.db = int(os.getenv("NEWS_REDIS_DB", 1))
        cls._redis_client = create_redis_client(config=redis_config)
        cls._landing_view_ttl = int(os.getenv("REDIS_LANDING_VIEW_TTL_SEC", MINUTE * 5))
        cls._news_data_ttl = int(os.getenv("REDIS_NEWS_DATA_TTL_DAYS", 120)) * DAY
        return cls._redis_client

    @classmethod
    def _get_redis_client(cls):
        if cls._redis_client:
            return cls._redis_client
        return cls._get_redis_connection()

    @classmethod
    def set_news_data(cls, token: str, data):
        client = cls._get_redis_client()
        client.set(token, data, ex=cls._news_data_ttl)

    @classmethod
    def get_news_data(cls, token: str):
        client = cls._get_redis_client()
        return client.get(token).decode()
