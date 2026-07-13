from app.services.gemini import GeminiService
from app.ai.prompts import SYSTEM_PROMPT


class DotBrain:

    def __init__(self):

        self.gemini = GeminiService()

    def chat(self, message: str):

        prompt = f"""
{SYSTEM_PROMPT}

User:
{message}
"""

        return self.gemini.generate(prompt)