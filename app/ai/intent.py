import json


class IntentDetector:

    def __init__(self, gemini):

        self.gemini = gemini


    def detect(self, message):

        prompt = f"""
Analisis pesan user berikut dan tentukan intent-nya.

Pesan user:

{message}

Gunakan salah satu intent:

1. chat
2. search_file

Jika user meminta file, ambil nama atau keyword file.

Jawab HANYA dalam JSON valid:

{{
    "intent": "chat",
    "keyword": null
}}

atau:

{{
    "intent": "search_file",
    "keyword": "nama file atau keyword"
}}

Jangan tambahkan penjelasan lain.
"""


        response = self.gemini.generate(
            prompt
        )


        try:

            cleaned = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


            return json.loads(
                cleaned
            )


        except Exception as error:

            print(
                "Intent detection error:",
                error
            )


            return {
                "intent": "chat",
                "keyword": None
            }