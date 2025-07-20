import json
from typing import Dict, List

import pymupdf
from db.redis.redis import RedisClient
from loguru import logger

from app.utils.env_encoder import get_settings
from app.utils.gemini_connector import GeminiConnector, ResumeParser

gemini_connector = GeminiConnector(api_key=get_settings().GEMINI_API_KEY)
resume_parser = ResumeParser(gemini_connector=gemini_connector)


def parse_pdf() -> List[Dict]:
    r = RedisClient()
    parsed_data = []

    doc = pymupdf.open(get_settings().PDF_INPUT_PATH)
    for page in doc:
        name = page.get_text("text").split("\n")[0].replace("\xa0", " ")
        value = r.get(name)
        if value:
            json_output = json.loads(value)
        else:
            json_output = resume_parser.parse_resume_to_json(page.get_text())
            if json_output:
                logger.info("✅ Successfully parsed resume to JSON format.")
                r.set(json_output.get("name"), json.dumps(json_output))
        parsed_data.append(json_output)
    doc.close()
    return parsed_data


def output_parsed_data() -> None:
    """
    Outputs the parsed data to a JSON file.
    """
    try:
        data = parse_pdf()
        with open(get_settings().PDF_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"✅ Successfully wrote parsed JSON data to: {get_settings().PDF_OUTPUT_PATH}")
    except IOError as e:
        logger.error(f"❌ Error writing to output file {get_settings().PDF_OUTPUT_PATH}: {e}")
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    output_parsed_data()
