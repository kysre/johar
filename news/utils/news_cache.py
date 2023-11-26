import os
import json

from clients.cache.redis import RedisConfig, create_redis_client

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


class NewsCache:
    _redis_client = None
    _landing_view_ttl = None
    _news_data_ttl = None
    _news_landing_view_key = 'NEWS_LANDING_PAGE'

    @classmethod
    def _get_redis_connection(cls):
        redis_config = RedisConfig()
        redis_config.db = int(os.getenv("NEWS_REDIS_DB", 1))
        cls._redis_client = create_redis_client(config=redis_config)
        cls._landing_view_ttl = int(os.getenv("REDIS_LANDING_VIEW_TTL_SEC", MINUTE * 10))
        cls._news_data_ttl = int(os.getenv("REDIS_NEWS_DATA_TTL_DAYS", 120)) * DAY
        return cls._redis_client

    @classmethod
    def _get_redis_client(cls):
        if cls._redis_client:
            return cls._redis_client
        return cls._get_redis_connection()

    @classmethod
    def _set_key_value(cls, key, value, ex):
        encoded_data = json.dumps(value).encode('utf-8')
        client = cls._get_redis_client()
        client.set(key, encoded_data, ex=ex)

    @classmethod
    def _get_value(cls, key):
        client = cls._get_redis_client()
        data = client.get(key)
        if data is not None:
            data = json.loads(data.decode())
        return data

    @classmethod
    def set_news_data(cls, token: str, news_data):
        cls._set_key_value(token, news_data, cls._news_data_ttl)

    @classmethod
    def get_news_data(cls, token: str):
        return cls._get_value(token)

    @classmethod
    def set_news_landing_page(cls, landing_page_data):
        cls._set_key_value(cls._news_landing_view_key, landing_page_data, cls._landing_view_ttl)

    @classmethod
    def get_news_landing_page(cls):
        return cls._get_value(cls._news_landing_view_key)
