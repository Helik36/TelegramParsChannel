import telegram
import asyncio
from tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID

from telegram import Update
from telegram._message import Message
from telegram._utils.types import CorrectOptionID, FileInput, JSONDict, ODVInput, ReplyMarkup
from typing import (Union, )

from telegram.ext import Application, Updater, CommandHandler, filters

token_bot = TOKEN
my_id = MY_ID
my_channel_id = MY_CHANNEL_ID


bot = telegram.Bot(TOKEN)


# Получаем информацию о последнем собщении
async def getMessId():
    bot = telegram.Bot(TOKEN)
    async with bot:
        updates = (await bot.get_updates())[-1]
        print(updates)
        print(updates.message.message_id)
        return updates.message.message_id

# async def deforwMess(chann_id, my, messid) -> None:
#     async with bot:
#         await bot.forward_message(chann_id, my, messid)

async def defCopyMess(chann_id, my, messid) -> None:
    async with bot:
        await bot.copyMessage(chann_id, my, messid)


async def startPoint():
    mess_id = await getMessId()
    # await deforwMess(channel_id, my_id, mess_id)
    await defCopyMess(my_channel_id, my_id, mess_id)

if __name__ == "__main__":
    asyncio.run(startPoint())
