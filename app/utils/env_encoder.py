import os
from functools import lru_cache

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PDF_INPUT_PATH = os.getenv("PDF_INPUT_PATH")
    PDF_OUTPUT_PATH = os.getenv("PDF_OUTPUT_PATH")


@lru_cache
def get_settings():
    return Settings()
