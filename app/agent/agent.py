from app.services.gemini_service import client
from app.agent.prompts import SYSTEM_PROMPT
from app.config import settings


class DotAgent:

    def chat(self, message: str):

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=f"""
{SYSTEM_PROMPT}

User:
{message}
"""
        )

        return response.text