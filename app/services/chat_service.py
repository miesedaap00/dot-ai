from openai import OpenAI

from app.config.settings import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


SYSTEM_PROMPT = """
You are Dot AI.

You are intelligent.

Helpful.

Friendly.

Professional.

Always answer in Indonesian unless user requests another language.
"""


def ask_ai(message: str):

    response = client.responses.create(

        model="gpt-5.5",

        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.output_text