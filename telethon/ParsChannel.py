from tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL
from async_cmd import input_cmd
from correctionTextForPars import correction_text
from additional_files.notNeededWords import upd_stop_post
from actionWithDB import db_parschannel, get_from_db_parschannel

import telethon
from telethon import TelegramClient, events
import logging
import asyncio

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

"""
Парсим сообщение. Переселываем в канал

Задачи:

1. Придумать задачи

3. Добавить возжожность добавлять/удалять каналы

4. Сделать инструкцию

7. Добавить чат бот-модератор

"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')
channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL

channel_from_pars = asyncio.run(db_parschannel())
names_channel = asyncio.run(get_from_db_parschannel())


# Проверка, что если присутствует слово, пост игнорируется
async def filter_text(event):
    for word in await upd_stop_post():
        if word in event.message.message.lower():
            return False
    return True


@client.on(events.NewMessage(func=filter_text))
async def parsing_new_message(event):
    if int(f"-100{event.message.peer_id.channel_id}") in await db_parschannel():

        # hasattr() принимает два аргумента: объект и имя атрибута в виде строки.
        # Функция возвращает True, если у объекта есть атрибут с указанным именем, и False в противном случае.
        if event.message.message != "":
            if hasattr(event.message.peer_id, "channel_id"):
                if int(f"-100{event.message.peer_id.channel_id}") in list(names_channel):
                    print(names_channel[int(f"-100{event.message.peer_id.channel_id}")])  # Тут словарь

        parsing_text = event.message
        parsing_text = await correction_text(parsing_text)

        if event.grouped_id:
            return  # ignore messages that are gallery here

        # Пояснение зачем тут try except:
        # По умолчанию, если отправляется фотка, к ней можно приложить текст с не более 1024 символов. Иначе будет ошибка
        # Решение: 1) Чтобы этого избежать, нужен премиум, он даёт 2048 символов. 2) Либо отправлять картинку как ссылку
        # Если текста нет вообще, сообщение может не отправиться. Проверить и подумать
        try:
            await client.send_message(channel_PL, parsing_text)
        except telethon.errors.rpcerrorlist.MediaCaptionTooLongError:
            print("В тексте больше 1024 символов. Пост игнорируется")


@client.on(events.Album())
async def parsing_almun(event):
    if int(f"-100{event.original_update.message.peer_id.channel_id}") in await db_parschannel():

        print("Норм")
        # Если отправляется альбом, в первом объекте текста может не быть, делаем проверку
        if not event.original_update.message.message:
            caption = event.messages[-1].message
            await client.send_file(channel_PL, event.messages, caption=caption)
        else:
            caption = event.original_update.message.message
            await client.send_file(channel_PL, event.messages, caption=caption)


async def start_bot():
    await client.start()
    await client.run_until_disconnected()


async def main():
    task1 = asyncio.create_task(start_bot())
    task2 = asyncio.create_task(input_cmd())

    tasks = [task1, task2]

    try:
        await asyncio.gather(*tasks)
    except:
        KeyboardInterrupt()


if __name__ == "__main__":
    asyncio.run(main())
