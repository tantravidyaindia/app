import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Logging
logging.basicConfig(level=logging.INFO)

# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # Your Firebase service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

# Your link prefix
LINK_PREFIX = "https://tantravidya.ct.ws/post.html?id="

# Command handlers
def start(bot, update):
    update.message.reply_text("Welcome! Use /search <title> to find posts.")

def search(bot, update, args):
    if not args:
        update.message.reply_text("Please provide a title to search.")
        return

    search_text = " ".join(args).strip()
    docs = db.collection("entries").stream()

    for doc in docs:
        data = doc.to_dict()
        if search_text.lower() in data.get("title", "").lower():
            update.message.reply_text(
                f"📄 {data.get('title')}\n🔗 {LINK_PREFIX}{doc.id}"
            )
            return

    update.message.reply_text("No matching post found.")

# Start the bot
if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search, pass_args=True))

    updater.start_polling()
    updater.idle()
