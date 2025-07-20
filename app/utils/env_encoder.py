import os
from functools import lru_cache

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PDF_INPUT_PATH = os.getenv("PDF_INPUT_PATH")
    PDF_OUTPUT_PATH = os.getenv("PDF_OUTPUT_PATH")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_USERNAME = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


@lru_cache
def get_settings():
    return Settings()
