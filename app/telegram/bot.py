from telegram import Update

from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)

from app.services.chat_service import ask_ai

from app.config.settings import settings


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    answer = ask_ai(user_message)

    await update.message.reply_text(answer)


def run_bot():

    app = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot Running...")

    app.run_polling()