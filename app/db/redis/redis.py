from typing import Optional

import redis
from loguru import logger

from app.utils.env_encoder import get_settings


class RedisClient:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=get_settings().REDIS_HOST,
                port=get_settings().REDIS_PORT,
                username=get_settings().REDIS_USERNAME,
                decode_responses=True,
                password=get_settings().REDIS_PASSWORD,
            )
            logger.info("✅ Connected to Redis.")
        except Exception as redis_e:
            logger.error(f"❌ Error connecting to Redis: {redis_e}")
            raise

    def set(self, key: str, value: str):
        try:
            if key is None or value is None:
                raise ValueError("Key or value must not be None.")
            self.client.set(key, value)
            logger.info(f"✅ Set key {key} in Redis.")
        except Exception as e:
            logger.error(f"❌ Error setting key {key} in Redis: {e}")
            raise

    def get(self, key: str) -> Optional[str]:
        try:
            if key is None:
                raise ValueError("Key must not be None.")
            value = self.client.get(key)
            if not value:
                logger.warning(f"⚠️ Key {key} not found in Redis.")
                return None
            logger.info(f"✅ Retrieved key {key} from Redis.")
            return value
        except Exception as e:
            logger.error(f"❌ Error getting key {key} from Redis: {e}")
            raise
