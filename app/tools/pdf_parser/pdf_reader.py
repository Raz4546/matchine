import json
import re
from typing import Dict, List, Union

import pymupdf
from db.redis.redis_handler import RedisClient
from loguru import logger

from app.utils.env_encoder import get_settings
from app.utils.gemini_connector import GeminiConnector, ResumeParser

gemini_connector = GeminiConnector(api_key=get_settings().GEMINI_API_KEY)
resume_parser = ResumeParser(gemini_connector=gemini_connector)


def find_email_address(text: str) -> Union[str, None]:
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = None
    for row in text.split("\n"):
        if re.search(email_pattern, row):
            match = re.search(email_pattern, row)
            break

    return match.group() if match else None


def parse_pdf() -> List[Dict]:
    r = RedisClient()
    parsed_data = []
    doc = pymupdf.open(get_settings().PDF_INPUT_PATH)
    for page in doc:
        value = r.client.get(find_email_address(page.get_text()))
        if value:
            json_output = json.loads(value)
        else:
            json_output = resume_parser.parse_resume_to_json(page.get_text())
            if json_output:
                logger.info("✅ Successfully parsed resume to JSON format.")
                r.client.set(json_output.get("mail"), json.dumps(json_output))
        parsed_data.append(json_output)
    doc.close()
    return parsed_data


def output_parsed_data() -> None:
    try:
        data = parse_pdf()
        with open(get_settings().PDF_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"✅ Successfully wrote parsed JSON data to: {get_settings().PDF_OUTPUT_PATH}")
    except IOError as e:
        logger.error(f"❌ Error writing to output file {get_settings().PDF_OUTPUT_PATH}: {e}")
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred: {e}")

