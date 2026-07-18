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


    def extract_memories(self, message: str):

        prompt = f"""
Analisis pesan user berikut.

Tentukan apakah terdapat informasi pribadi atau preferensi
yang layak disimpan sebagai memory jangka panjang.

Pesan user:

{message}

Jika ada informasi penting, jawab HANYA dengan format JSON valid:

{{
    "memories": [
        {{
            "key": "nama_key",
            "value": "nilai"
        }}
    ]
}}

Jika tidak ada informasi penting, jawab:

{{
    "memories": []
}}

Jangan tambahkan penjelasan lain.
"""

        response = self.client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt
        )

        return response.text