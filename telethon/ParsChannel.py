from tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL
from telethon import TelegramClient

import time
import logging


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash)

id_for_pars_channel = -1001201194408  # Мир PS
channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL


async def parsingChannel():
    # Получаем последние сообщения
    # Лимит показывает отправленные объекты. Т.е в телеге может быть 1 сообщение, у него есть 2 фото и текст. Это 3 разных объекта
    # Далее работается также как и с get_message
    pasring_photos = []  # Сюда можно положить несколько фото и разом отправить в client.send_file
    pasring_text = []
    async for data_message in client.iter_messages(channel_test, limit=2):

        # Если фото присутстует, добавить в массив, иначе ничего не делать
        if data_message.photo is not None:
            pasring_photos.append(data_message.photo)
        else:
            pass

        # Если текст не пустой, добавить в массив, иначе ничего не делать
        if data_message.message != '':
            pasring_text.append(data_message.message)
        else:
            pass

    await client.send_file(channel_PL, pasring_photos, caption=pasring_text[0])

    print("Done")
    time.sleep(3)

    print(pasring_text)
    print(pasring_photos[0])
    print(pasring_photos[1])


async def main():
    await parsingChannel()


with client:
    client.loop.run_until_complete(main())

    """
    Парсим сообщение. Переселываем в канал
    
    Задачи:
    1. Чтобы скрипт работал пока не отключу сам.
    
    2. Если скрипт будет активен постоянно, обдумать, как запускать процесс парсинга при новых сообщениях
    (т.е иными словами, чтобы не получилось так, что парситься одно и тоже сообщение
    """
