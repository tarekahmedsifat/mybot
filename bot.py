from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler)
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# commands

async def start(update : Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👍 Like", callback_data="like")],
        [InlineKeyboardButton("👎 Dislike", callback_data="dislike")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to our community!", reply_markup=reply_markup)

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Counting: 🔟")
    for x in ['9️⃣','8️⃣','7️⃣','6️⃣','5️⃣','4️⃣','3️⃣','2️⃣','1️⃣','0️⃣']:
        await msg.edit_text(f"Counting: {x}")
        await asyncio.sleep(0.6)
    await msg.edit_text("Countdown finished!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")
    

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "like":
        await query.edit_message_text(text="You clicked 👍 Like!")
    else:
        await query.edit_message_text(text="You clicked 👎 Dislike!")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('countdown', countdown))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

print("Bot is running fine......")
app.run_polling()