from datetime import datetime, timedelta
import random

from tokens.tokens import API_ID, API_HASH
from actionWithCMD import input_cmd
from correctionTextForPars import correction_text
from additional_files.notNeededWords import upd_stop_post
from database.actionWithDB import (db_get_id_parschannel, get_from_db_parschannel, get_my_id_channel,
                                   get_time_pause_post, set_new_time_pause_post)

import telethon
from telethon import TelegramClient, events
import logging
import asyncio

logging.basicConfig(filename='logs/app.log',
            format="\n[%(asctime)s]: %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            level=logging.INFO)

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('database/anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')


# Проверка, что если присутствует слово, пост игнорируется и что прошло некоторое время
async def filter_text(event):

    try:
        old_pause_post = await get_time_pause_post()

        if event.message.post and int(f"-100{event.message.peer_id.channel_id}") in await db_get_id_parschannel():

            if str(datetime.now()) > old_pause_post:

                # Это временная мера для эксплоит. Нужно добавить отдельно в базу
                # upd: Ломается логика работы скрипта, если в посте есть и пикча и видео
                if not hasattr(event.message.media, "video") or event.message.media.video != True:

                    for word in await upd_stop_post():

                        if word.lower() in event.message.message.lower():
                            logging.info(f"\nБлок Пост. В посте присутствует стоп-слово - {word.lower()}\n")
                            return False

                    # Пауза между постами
                    # UPD - Если в посте больше 1 файла (фото, видио) блокирует вообще пост. Подумать
                    # minute_time = random.randint(60, 90)
                    # new_time = datetime.now() + timedelta(minutes=minute_time)
                    # logging.info(f"Установлена пазу на {minute_time} минут. Следующий пост доступен после {new_time} "
                    #              f"(МСК - {new_time + timedelta(hours=3)}\n")

                    # await set_new_time_pause_post(str(new_time))

                    return True

                logging.info(f"Блок Пост. Присутствует видео\n")
                return False

            logging.info(f"Блок Пост. Пост доступен после {old_pause_post} (МСК +3 часа)\n")
            return False

    except:
        pass


@client.on(events.NewMessage(func=filter_text))
async def parsing_new_message(event):

    # hasattr() принимает два аргумента: объект и имя атрибута в виде строки.
    # Функция возвращает True, если у объекта есть атрибут с указанным именем, и False в противном случае.
    
    event.message.entities.clear() # Удаляет гиперссылки
    parsing_text = event.message


    if event.message.message != "":

        parsing_text = await correction_text(parsing_text)


    if event.grouped_id:
        return  # ignore messages that are gallery here

    # Пояснение зачем тут try except:
    # По умолчанию, если отправляется фотка, к ней можно приложить текст с не более 1024 символов. Иначе будет ошибка
    # Решение: 1) Чтобы этого избежать, нужен премиум, он даёт 2048 символов. 2) Либо отправлять картинку как ссылку
    try:

        for my_channel in await get_my_id_channel():
            await client.send_message(my_channel, parsing_text)

    except telethon.errors.rpcerrorlist.MediaCaptionTooLongError:
        logging.info("В тексте больше 1024 символов. Пост игнорируется")


async def filter_text_album(event):

    old_pause_post = await get_time_pause_post()

    if int(f"-100{event.original_update.message.peer_id.channel_id}") in await db_get_id_parschannel():

        if str(datetime.now()) > old_pause_post:
            logging.info(f"Блок Пост. Пост доступен после {old_pause_post} (МСК +3 часа)\n")

            # Не помню для чего. Уточнить
            if not event.original_update.message.message:
                for word in await upd_stop_post():
                    if word.lower() in event.messages[-1].message.lower():
                        logging.info(f"Блок Пост. В посте присутствует слово - {word.lower()}\n")
                        return False

            else:
                for word in await upd_stop_post():
                    if word.lower() in event.original_update.message.message.lower():
                        logging.info(f"Блок Пост. В посте присутствует слово - {word.lower()}\n")
                        return False

            return True


@client.on(events.Album(func=filter_text_album))
async def parsing_almun(event):

    # Если отправляется альбом, в первом объекте текста может не быть, делаем проверку

    if not event.original_update.message.message:
        caption = event.messages[-1].message

        for my_channel in await get_my_id_channel():
            await client.send_file(my_channel, event.messages, caption=caption)

    else:
        caption = event.original_update.message.message

        for my_channel in await get_my_id_channel():
            await client.send_file(my_channel, event.messages, caption=caption)


async def start_script():
    await client.start()
    await client.run_until_disconnected()


async def main():
    task1 = asyncio.create_task(start_script())
    task2 = asyncio.create_task(input_cmd())

    tasks = [task1, task2]

    try:
        await asyncio.gather(*tasks)
    except:
        KeyboardInterrupt()


if __name__ == "__main__":
    asyncio.run(main())
