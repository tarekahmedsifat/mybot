import os
import asyncio
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-app.onrender.com/webhook

# -------------------
# Telegram Handlers
# -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👍 Like", callback_data="like")],
        [InlineKeyboardButton("👎 Dislike", callback_data="dislike")]
    ]
    await update.message.reply_text(
        "Welcome to the bot!", reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "like":
        await query.edit_message_text("You clicked 👍 Like!")
    else:
        await query.edit_message_text("You clicked 👎 Dislike!")

# -------------------
# FastAPI App
# -------------------
app = FastAPI()

# Create Telegram Application
bot_app = ApplicationBuilder().token(TOKEN).build()

# Add handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
bot_app.add_handler(CallbackQueryHandler(button_handler))

# Webhook endpoint
@app.post("/webhook")
async def telegram_webhook(update: dict):
    tg_update = Update.de_json(update, bot_app.bot)
    await bot_app.update_queue.put(tg_update)
    return {"ok": True}

# Startup: initialize bot and set webhook
@app.on_event("startup")
async def startup_event():
    await bot_app.initialize()  # initialize bot properly
    await bot_app.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook successfully set to: {WEBHOOK_URL}")
