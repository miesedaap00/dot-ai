import os
import mimetypes
import re

from telegram import Update

from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.ai.brain import DotBrain
from app.config import config
from app.services.google_drive import GoogleDriveService
from app.services.file_database import FileDatabase


brain = DotBrain()

drive = GoogleDriveService()

file_database = FileDatabase()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    chat_id = update.effective_chat.id


    intent = brain.detect_intent(
        text
    )


    if intent["intent"] == "search_file":

        keyword = intent.get(
            "keyword"
        )


        if not keyword:

            await update.message.reply_text(
                "❌ Saya belum tahu file mana yang ingin dicari."
            )

            return


        await send_file_back(
            update,
            keyword
        )

        return


    answer = brain.chat(
        chat_id,
        text
    )


    await update.message.reply_text(
        answer
    )


async def handle_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    document = update.message.document

    file_name = document.file_name

    file_id = document.file_id

    file = await context.bot.get_file(
        file_id
    )

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    local_path = os.path.join(
        "uploads",
        file_name
    )

    await file.download_to_drive(
        local_path
    )

    mime_type = (
        document.mime_type
        or mimetypes.guess_type(file_name)[0]
        or "application/octet-stream"
    )

    await update.message.reply_text(
        "⏳ File sedang disimpan ke Google Drive..."
    )

    uploaded_file = drive.upload_file(
        file_path=local_path,
        file_name=file_name,
        mime_type=mime_type
    )
    
    file_database.save_file(

        user_id=update.effective_chat.id,

        file_name=uploaded_file["name"],

        drive_file_id=uploaded_file["id"],

        mime_type=uploaded_file["mimeType"],

        drive_link=uploaded_file.get(
            "webViewLink"
        )
    )

    os.remove(
        local_path
    )

    await update.message.reply_text(
        f"✅ File berhasil disimpan ke Google Drive!\n\n"
        f"📄 {uploaded_file['name']}"
    )


async def handle_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    photo = update.message.photo[-1]

    file_id = photo.file_id

    file = await context.bot.get_file(
        file_id
    )

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    local_path = os.path.join(
        "uploads",
        f"{file_id}.jpg"
    )

    await file.download_to_drive(
        local_path
    )

    await update.message.reply_text(
        "⏳ Gambar sedang disimpan ke Google Drive..."
    )

    uploaded_file = drive.upload_file(
        file_path=local_path,
        file_name=f"{file_id}.jpg",
        mime_type="image/jpeg"
    )
    
    file_database.save_file(

        user_id=update.effective_chat.id,

        file_name=uploaded_file["name"],

        drive_file_id=uploaded_file["id"],

        mime_type=uploaded_file["mimeType"],

        drive_link=uploaded_file.get(
            "webViewLink"
        )
    )

    os.remove(
        local_path
    )

    await update.message.reply_text(
        f"✅ Gambar berhasil disimpan ke Google Drive!\n\n"
        f"🖼️ {uploaded_file['name']}"
    )


async def send_file_back(
    update,
    file_name
):

    chat_id = update.effective_chat.id

    result = file_database.search_best_file(
        chat_id,
        file_name
    )

    if not result:

        await update.message.reply_text(
            f"❌ File `{file_name}` tidak ditemukan."
        )

        return


    (
        saved_file_name,
        drive_file_id,
        mime_type,
        drive_link,
        created_at
    ) = result


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    local_path = os.path.join(
        "uploads",
        saved_file_name
    )


    await update.message.reply_text(
        "⏳ File sedang diambil dari Google Drive..."
    )


    drive.download_file(
        file_id=drive_file_id,
        destination_path=local_path
    )


    await update.message.reply_text(
        "📤 File sedang dikirim kembali..."
    )


    await update.message.reply_document(
        document=open(
            local_path,
            "rb"
        ),
        filename=saved_file_name
    )


    os.remove(
        local_path
    )

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


    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_document
        )
    )


    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )


    print(
        "🤖 Dot AI is running..."
    )


    app.run_polling()