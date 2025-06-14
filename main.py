import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # MAKE SURE THIS FILE EXISTS
firebase_admin.initialize_app(cred)
db = firestore.client()

# Your link prefix
LINK_PREFIX = "https://tantravidya.ct.ws/post.html?id="

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /search <title> to find posts.")

# /search command
def search(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please provide a title to search.")
        return
    
    search_text = " ".join(context.args).strip()
    docs = db.collection("entries").stream()

    for doc in docs:
        data = doc.to_dict()
        if search_text.lower() in data.get("title", "").lower():
            update.message.reply_text(
                f"📄 {data.get('title')}\n🔗 {LINK_PREFIX}{doc.id}"
            )
            return
    
    update.message.reply_text("No matching post found.")

# Setup bot
if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))

    updater.start_polling()
    updater.idle()
