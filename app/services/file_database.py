from app.services.database import get_connection


class FileDatabase:


    def save_file(

        self,

        user_id,

        file_name,

        drive_file_id,

        mime_type,

        drive_link

    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO files (

                user_id,

                file_name,

                drive_file_id,

                mime_type,

                drive_link

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            str(user_id),

            file_name,

            drive_file_id,

            mime_type,

            drive_link

        ))


        conn.commit()

        conn.close()


    def search_files(

        self,

        user_id,

        keyword

    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute("""
            SELECT

                file_name,

                drive_file_id,

                mime_type,

                drive_link,

                created_at

            FROM files

            WHERE user_id = ?

            AND file_name LIKE ?

            ORDER BY created_at DESC

        """, (

            str(user_id),

            f"%{keyword}%"

        ))


        results = cursor.fetchall()


        conn.close()


        return results
    
    def search_best_file(
        self,
        user_id,
        keyword
    ):

        results = self.search_files(
            user_id,
            keyword
        )

        if results:

            return results[0]

        return None