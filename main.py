import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # ADD THIS FILE (read notes)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Your link prefix
LINK_PREFIX = "https://tantravidya.ct.ws/post.html?id="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /search <title> to find posts.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
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

# Setup bot
app = ApplicationBuilder().token(os.getenv("8189883530:AAF36-GgsU8gEbJblP-qQpbwM3cAozHq6pM")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

# Run
if __name__ == "__main__":
    app.run_polling()
