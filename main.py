import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Logging
logging.basicConfig(level=logging.INFO)

# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # Keep this file safe
firebase_admin.initialize_app(cred)
db = firestore.client()

# Your link prefix
LINK_PREFIX = "https://tantravidya.ct.ws/post.html?id="

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /search <title> to find posts.")

# Search command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a title to search.")
        return

    search_text = " ".join(context.args).strip()
    docs = db.collection("entries").stream()

    for doc in docs:
        data = doc.to_dict()
        if search_text.lower() in data.get("title", "").lower():
            await update.message.reply_text(
                f"📄 {data.get('title')}\n🔗 {LINK_PREFIX}{doc.id}"
            )
            return

    await update.message.reply_text("No matching post found.")

# Main app
if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    app.run_polling()
