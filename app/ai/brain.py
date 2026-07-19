from app.services.gemini import GeminiService

from app.ai.prompts import SYSTEM_PROMPT

from app.ai.history import ConversationHistory

from app.ai.memory import MemoryManager

from app.ai.intent import IntentDetector


class DotBrain:

    def __init__(self):

        self.gemini = GeminiService()

        self.history = ConversationHistory()

        self.memory = MemoryManager()
        
        self.intent_detector = IntentDetector(
            self.gemini
        )
        
    def detect_intent(
        self,
        message
    ):

        return self.intent_detector.detect(
            message
        )

    def chat(
        self,
        chat_id: int,
        message: str
    ):

        memories = self.memory.get_all(
            chat_id
        )


        memory_text = ""

        for key, value in memories:

            memory_text += (
                f"{key}: {value}\n"
            )


        conversation = self.history.get_history(
            chat_id
        )


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

        Jawab pesan user dengan mempertimbangkan
        memory dan riwayat percakapan.
        """


        answer = self.gemini.generate(
            prompt
        )


        self.memory.extract_and_save(
            chat_id,
            self.gemini,
            message
        )


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