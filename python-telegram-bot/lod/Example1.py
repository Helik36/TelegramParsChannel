import asyncio
import telegram
from ..tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID

token_bot = TOKEN
my_id = MY_ID

# 1 Check that the credentials are correct
# Used for getting basic information about the bot
async def main1():
    bot = telegram.Bot(token_bot)
    async with bot:
        print(await bot.get_me())

# 2 Get id from user
# Used for getting updates using long polling
async def main2():
    bot = telegram.Bot(token_bot)
    async with bot:
        updates = (await bot.get_updates())[-1]
        print(updates)
        print(updates.message.message_id)


# Send message use id
async def main3():
    bot = telegram.Bot(token_bot)
    async with bot:
        await bot.send_message(text='Hi!', chat_id= my_id )



if __name__ == '__main__':
    # asyncio.run(main1())
    asyncio.run(main2())
    # asyncio.run(main3())

