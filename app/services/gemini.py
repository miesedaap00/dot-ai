from google import genai
from google.genai.errors import ServerError

from app.config import config


class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

    def generate(self, prompt: str):

        try:
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt
            )

            return response.text

        except ServerError:
            return (
                "⚠️ Maaf, server AI sedang sibuk. "
                "Silakan coba lagi beberapa saat."
            )

        except Exception as e:
            print(e)
            return "Terjadi kesalahan."