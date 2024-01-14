from Examples.tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL
from telethon import TelegramClient, events

import time
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

"""
Парсим сообщение. Переселываем в канал

Задачи:
1. Чтобы скрипт работал пока не отключу сам.

2. Если скрипт будет активен постоянно, обдумать, как запускать процесс парсинга при новых сообщениях
(т.е иными словами, чтобы не получилось так, что парситься одно и тоже сообщение)

3. Обдумать процесс по количеству парсинга сообщений (лимит) (вообще нужен ли)

4. last upd - не совсем корректно работает, может отправить картинку несколько раз, разобаться
"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

id_for_pars_channel = -1001201194408  # Мир PS
channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL

# Добавил обработчик событый, указал, что нужно реагировать, если приходят новые сообщения из channel_test
@client.on(events.NewMessage(chats=channel_test))
async def parsingChannel(event):
    # Получаем последние сообщения Лимит показывает отправленные объекты. Т.е в телеге может быть 1 сообщение,
    # у него есть 2 фото и текст. Это 3 разных объекта Далее работается также как и с get_message
    pasring_photos = []  # Сюда можно положить несколько фото и разом отправить в client.send_file
    pasring_text = []
    print("wait event")
    print(f"event -- {event}")
    print(f"event.message -- {event.message}")
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
    time.sleep(10)

    # print(pasring_text)
    # print(pasring_photos[0])
    # print(pasring_photos[1])


# async def main():
#     await parsingChannel()


client.start()
client.run_until_disconnected()


