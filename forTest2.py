import telegram
import asyncio

from telegram import Update
from telegram._message import Message
from telegram._utils.types import CorrectOptionID, FileInput, JSONDict, ODVInput, ReplyMarkup
from typing import (Union, )

from telegram.ext import Application, Updater, CommandHandler, filters

TOKEN = "token"
my_id = "0123"
channel_id = "-0123"

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
    await defCopyMess(channel_id, my_id, mess_id)

if __name__ == "__main__":
    asyncio.run(startPoint())
