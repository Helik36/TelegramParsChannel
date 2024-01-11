import asyncio
import telegram

TOKEN = "token"
id = 123

# 1 Check that the credentials are correct
# Used for getting basic information about the bot
async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        print(await bot.get_me())

# 2 Get id from user
# Used for getting updates using long polling
async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        updates = (await bot.get_updates())[-1]
        print(updates)
        print(updates.message.message_id)


# Send message use id
async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        await bot.send_message(text='Hi!', chat_id= id )



if __name__ == '__main__':
    asyncio.run(main())

