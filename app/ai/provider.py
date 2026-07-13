from google import genai

from app.config.settings import settings


class GeminiProvider:

    def __init__(self):

        self.client = genai.Client(

            api_key=settings.GEMINI_API_KEY
        )

    def generate(self, prompt):

        response = self.client.models.generate_content(

            model=settings.GEMINI_MODEL,

            contents=prompt

        )

        return response.text