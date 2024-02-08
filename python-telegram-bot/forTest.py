import asyncio
import logging
from telegram.ext import CommandHandler, ConversationHandler, ApplicationBuilder
from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID

token_bot = TOKEN
my_id = MY_ID
my_channel_id = MY_CHANNEL_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
id_channel_pasring = ID_CHANNEL_ID


# Вызывается по команде
async def start(update, _):
    await update.message.reply_text('Kek')


async def main():
    application = ApplicationBuilder().token(token_bot).build()

    print("qweqew")



    async with application:  # Calls `initialize` and `shutdown`
        await application.start()
        await application.updater.start_polling()

        await application.add_handler(CommandHandler("start", start))

        await application.updater.stop()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
