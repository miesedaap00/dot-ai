from app.services.gemini import GeminiService
from app.ai.prompts import SYSTEM_PROMPT
from app.ai.history import ConversationHistory
from app.ai.memory import MemoryManager


class DotBrain:

    def __init__(self):

        self.gemini = GeminiService()

        self.history = ConversationHistory()

        self.memory = MemoryManager()


    def chat(self, chat_id: int, message: str):

        conversation = self.history.get_history(chat_id)

        memories = self.memory.get_all(chat_id)

        memory_text = ""

        for key, value in memories:

            memory_text += f"{key}: {value}\n"


        conversation_text = ""

        for item in conversation:

            conversation_text += (
                f"{item['role']}: "
                f"{item['content']}\n"
            )


        prompt = f"""
{SYSTEM_PROMPT}

INFORMASI PENTING TENTANG USER:

{memory_text}

RIWAYAT PERCAKAPAN:

{conversation_text}

PESAN USER:

{message}

Jawab berdasarkan informasi penting dan konteks percakapan.
"""


        answer = self.gemini.generate(prompt)


        self.history.add_message(
            chat_id,
            "User",
            message
        )


        self.history.add_message(
            chat_id,
            "Assistant",
            answer
        )


        return answer