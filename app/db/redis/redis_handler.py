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
