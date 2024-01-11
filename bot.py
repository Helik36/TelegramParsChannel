import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler

TOKEN = "token"
my_id = "0123"
channel_id = "-0123"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем информацию о последнем собщении
async def getMessId(update: Update, context):
    print(update.message)
    print(update.message.text)
    print(update.message.message_id)
    await context.bot.copyMessage(channel_id, my_id, update.message.message_id)

async def start_callback(update, context):
    await update.message.reply_text("Hello! I'm your bot.")

# async def deforwMess(chann_id, my, messid) -> None:
#     async with bot:
#         await bot.forward_message(chann_id, my, messid)

# async def defCopyMess(chann_id, my, messid) -> None:
#     async with bot:
#         await bot.copyMessage(chann_id, my, messid)

# async def startPoint():
#
#     mess_id = await getMessId()
#     print(mess_id)

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_callback))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), getMessId))
    app.run_polling()

if __name__ == "__main__":
    main()