from collections import defaultdict


class ConversationHistory:

    def __init__(self, max_messages=20):
        self.histories = defaultdict(list)
        self.max_messages = max_messages

    def add_message(self, chat_id, role, content):
        self.histories[chat_id].append({
            "role": role,
            "content": content
        })

        self.histories[chat_id] = (
            self.histories[chat_id][-self.max_messages:]
        )

    def get_history(self, chat_id):
        return self.histories[chat_id]

    def clear_history(self, chat_id):
        self.histories[chat_id] = []