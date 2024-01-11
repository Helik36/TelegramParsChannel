import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler

import bot

TOKEN = "token"

async def getMessId(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message)
    print(update.message.text)

async def start_callback(update, context):
    await update.message.reply_text("Hello! I'm your bot.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), getMessId))
    app.run_polling()

if __name__ == '__main__':
    main()