from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")


config = Config()