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

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL

# @client.on(events.NewMessage(chats='me'))
# async def handler(event):
#     print("message")
#     if event.grouped_id:
#         return    # ignore messages that are gallery here
#
#     await client.send_message(channel_test, event.message)

# Добавил обработчик событый, указал, что нужно реагировать, если приходят новые сообщения из channel_test
@client.on(events.Album(chats='me'))
async def handler(event):
    print("albom")
    pasring_photos = []  # Сюда можно положить несколько фото и разом отправить в client.send_file
    pasring_text = []
    unique_photo_hashes = set()  # нужен на провеку уникольности фото (т.к фотки могут повторяться

    # Получаем последние сообщения Лимит показывает отправленные объекты. Т.е в телеге может быть 1 сообщение,
    # у него есть 2 фото и текст. Это 3 разных объекта Далее работается также как и с get_message
    #
    # Если фото присутстует, добавить в массив, иначе ничего не делать
    if event.original_update.message.photo is not None:
        print('1 шаг - фото присутствует')
        hash_photo = event.original_update.message.id

        # Проверка, чтобы не добавлять дубли фоток
        if hash_photo not in unique_photo_hashes:
            pasring_photos.append(event.original_update.message.photo)
            unique_photo_hashes.add(hash_photo)
        else:
            print("Присутсвует дубль/дубли фото")

        # проверка, что сообщение не пустое
        if event.original_update.message.message != '':
            print('2 шаг - Сообщение не пустое')

            # Если текст не пустой, добавить в массив
            pasring_text.append(event.original_update.message.message)

    else:
        print('3 шаг - Фото отсутсвует, сообщение не пустое')
        if event.message != '':
            pasring_text.append(event.original_update.message.message)


    if not pasring_photos:
        print("\nОтправляет сообщение. Фото отсутсвуют, только текст")
        print(f"Текст - {pasring_text[0]}\n")
        await client.send_message(channel_test, message=event.original_update.message.message)

    elif not pasring_text:
        print("\nОтправляет сообщение. Только фото, текст отсутсвует")
        await client.send_file(channel_test, pasring_photos, caption='')

    else:
        print("\nОтправляет сообщение. Фото и текст")
        print(f"фото и Текст - {pasring_text[0]}\n")
        await client.send_file(channel_test, pasring_photos, caption=pasring_text[0])  # caption = подпись = message

        pasring_text.clear()
        pasring_photos.clear()
        unique_photo_hashes.clear()

    print("Done\n")
    time.sleep(5)
    print("sleep is compliet!")

client.start()
client.run_until_disconnected()
