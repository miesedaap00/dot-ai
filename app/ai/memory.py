import json

from app.services.database import get_connection


class MemoryManager:

    def save(self, user_id, key, value):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO memories (
                user_id,
                key,
                value
            )
            VALUES (?, ?, ?)

            ON CONFLICT(user_id, key)

            DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (
            str(user_id),
            key,
            value
        ))

        conn.commit()

        conn.close()


    def get(self, user_id, key):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT value
            FROM memories
            WHERE user_id = ?
            AND key = ?
        """, (
            str(user_id),
            key
        ))

        result = cursor.fetchone()

        conn.close()

        if result:

            return result[0]

        return None


    def get_all(self, user_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT key, value
            FROM memories
            WHERE user_id = ?
        """, (
            str(user_id),
        ))

        memories = cursor.fetchall()

        conn.close()

        return memories


    def extract_and_save(
        self,
        user_id,
        gemini,
        message
    ):

        raw_response = gemini.extract_memories(
            message
        )

        try:

            cleaned_response = (
                raw_response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            data = json.loads(
                cleaned_response
            )

            memories = data.get(
                "memories",
                []
            )

            for memory in memories:

                key = memory.get("key")

                value = memory.get("value")

                if key and value:

                    self.save(
                        user_id,
                        key,
                        value
                    )

        except Exception as error:

            print(
                "Memory extraction error:",
                error
            )