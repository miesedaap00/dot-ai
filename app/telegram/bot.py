from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.agent.agent import DotAgent
from app.config.settings import settings

agent = DotAgent()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.message is None or update.message.text is None:
        return

    user_message = update.message.text

    try:
        answer = agent.chat(user_message)

        await update.message.reply_text(answer)

    except Exception as e:
        print(e)

        await update.message.reply_text(
            "Maaf, Dot AI sedang mengalami gangguan."
        )


def run_bot():

    app = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("🤖 Dot AI is running...")

    app.run_polling()