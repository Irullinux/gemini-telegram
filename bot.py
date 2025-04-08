import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load token dari .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Fungsi kirim prompt ke Gemini 1.5 Pro (Gemini 2.5)
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        result = res.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"[Error Gemini] {e}"

# Handler saat user kirim pesan
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Tunggu sebentar, sedang berpikir...")
    reply = ask_gemini(user_text)
    await update.message.reply_text(reply)

# Main app
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot aktif...")
    app.run_polling()

if __name__ == "__main__":
    main()
