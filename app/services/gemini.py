from google import genai

from app.config import config


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

    def generate(self, prompt: str):

        response = self.client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt
        )

        return response.text