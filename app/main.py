from app.services.database import init_database


def start_app():

    init_database()

    print("Database initialized.")