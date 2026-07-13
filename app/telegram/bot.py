from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.ai.brain import DotBrain
from app.config import config

brain = DotBrain()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    answer = brain.chat(text)

    await update.message.reply_text(answer)


def run_bot():

    app = Application.builder().token(
        config.TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("🤖 Dot AI is running...")

    app.run_polling()