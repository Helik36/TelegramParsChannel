import asyncio
import logging
from telegram.ext import CommandHandler, ConversationHandler, ApplicationBuilder, Application
from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID
from ParsChannel import start_bot
from async_cmd import input_cmd

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


async def run():
    # task1 = asyncio.create_task(start_bot())
    # task2 = asyncio.create_task(input_cmd())
    #
    # tasks = [task1, task2]
    #
    # try:
    #     await asyncio.gather(*tasks)
    # except:
    #     KeyboardInterrupt()
    application = Application.builder().token(token_bot).build()

    print("qweqew")

    cmd_handler = CommandHandler("start", start)
    application.add_handler(cmd_handler)

    task1 = asyncio.create_task(start_bot())
    task2 = asyncio.create_task(input_cmd())

    tasks = [task1, task2]

    try:
        async with application:
            await application.initialize()
            await application.start()
            await application.updater.start_polling()
            await asyncio.gather(*tasks)
    except:
        KeyboardInterrupt()


if __name__ == "__main__":
    asyncio.run(run())
