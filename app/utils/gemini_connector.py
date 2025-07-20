import json
from typing import Dict

import google.generativeai as genai
from loguru import logger

from data.prompt_skeleton.prompts import Prompts

GEMINI_MODEL = "gemini-2.5-flash"  # Default model, can be changed as needed


class GeminiConnector:
    """
    A class to facilitate interaction with the Google Gemini API.
    Handles API key configuration and basic text/JSON generation.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key cannot be empty.")
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
            logger.info("✅ Gemini model initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini model: {e}")
            raise

    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            logger.error(f"❌ Failed to generate text from Gemini API: {e}")
            raise

    def generate_json(self, prompt: str, **kwargs) -> Dict:
        raw_response = self.generate_text(prompt, **kwargs)
        if not raw_response:
            logger.error("Received empty response from Gemini API.")
            raise
        try:
            if raw_response.strip().startswith("```json") and raw_response.strip().endswith("```"):
                json_string = raw_response.strip()[7:-3].strip()
            else:
                json_string = raw_response.strip()

            return json.loads(json_string)
        except json.JSONDecodeError as json_e:
            logger.error(f"❌ Failed to decode JSON from Gemini API response: {json_e}")
            raise
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred while processing the response: {e}")
            raise

    def generate_chat_response(self, chat_history: list, new_message: str, **kwargs) -> str:
        try:
            chat = self.model.start_chat(history=chat_history)
            response = chat.send_message(new_message, **kwargs)
            return response.text
        except Exception as e:
            logger.error(f"❌ Failed to generate chat response: {e}")
            raise

    def get_model_info(self) -> Dict:
        try:
            for m in genai.list_models():
                if m.name == f"models/{self.model.model_name}":
                    return m.to_dict()
            return {"message": f"Could not find detailed info for model: {self.model.model_name}"}
        except Exception as e:
            logger.error(f"❌ Failed to retrieve model info: {e}")
            raise


class ResumeParser:
    """
    A class to parse resume text into a structured JSON format using Gemini AI.
    It utilizes an instance of GeminiConnector.
    """

    def __init__(self, gemini_connector: GeminiConnector):
        if not isinstance(gemini_connector, GeminiConnector):
            logger.error("❌ gemini_connector must be an instance of GeminiConnector.")
            raise TypeError("gemini_connector must be an instance of GeminiConnector.")
        self.connector = gemini_connector

    def parse_resume_to_json(self, resume_text: str) -> Dict:
        prompt = Prompts.get_resume_to_json_prompt(resume_text)
        logger.info("🔃 Sending prompt to Gemini API via GeminiConnector...")
        try:
            resume_json = self.connector.generate_json(prompt)
            logger.info("✅ Successfully received and parsed JSON from Gemini.")
            return resume_json
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"❌ Failed to parse resume to JSON: {e}")
            raise
