import json

import pymupdf
from loguru import logger

from app.utils.env_encoder import get_settings
from app.utils.gemini_connector import GeminiConnector, ResumeParser

PDF_INPUT_PATH = get_settings().PDF_INPUT_PATH
PDF_OUTPUT_PATH = get_settings().PDF_OUTPUT_PATH

gemini_connector = GeminiConnector(api_key=get_settings().GEMINI_API_KEY)
resume_parser = ResumeParser(gemini_connector=gemini_connector)
parsed_data = []

doc = pymupdf.open(PDF_INPUT_PATH)
for page in doc:
    json_output = resume_parser.parse_resume_to_json(page.get_text())
    if json_output:
        logger.info("✅ Successfully parsed resume to JSON format.")
        parsed_data.append(json_output)
doc.close()

if parsed_data:
    try:
        with open(PDF_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=4, ensure_ascii=False)
        logger.info(f"✅ Successfully wrote parsed JSON data to: {PDF_OUTPUT_PATH}")
    except IOError as e:
        logger.error(f"❌ Error writing to output file {PDF_OUTPUT_PATH}: {e}")
else:
    logger.warning("⚠️ No data was successfully parsed to write to an output file.")
