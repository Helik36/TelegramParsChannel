import re

from Examples.tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL, CHANNEL_FROM_PARS
from telethon import TelegramClient, events
import emoji

import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

"""
Парсим сообщение. Переселываем в канал

Задачи:

1. Придумать задачи

2. Проверить работу при получении иных медиа, помимо фоток

3. После получения события, забирать сообщение, немного изменять его, и отправлять

4. Обдумать добавление тегов

5. Добавить фильтры для отсеивания постов (ссылки на вк, куда-то ещё

"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL
channel_from_pars = CHANNEL_FROM_PARS

# массив по которым будут удаляться ненужные слова
detele_word = ["#", "Для покупки с нашей помощью", "Цена в рублях указана при покупке с нашей помощью"]

# Срабатывает на сообщения и на сообщения с фото 1.

# @client.on(events.NewMessage(chats='me'))
@client.on(events.NewMessage(chats=channel_from_pars))
async def parsing_new_message(event):
    print("Сработал NewMessage\n")

    pasring_text = event.message

    for word in range(len(detele_word)):
        # .*? - любой текст. (\n \n|$) -Это группа захвата, которая соответствует или символу новой строки,
        # за которым следует пробел, за которым следует ещё один символ новой строки (\n \n), или концу строки ($).
        reg_text = re.escape(detele_word[word]) + r".*?(\n \n|$)"
        pasring_text.message = re.sub(reg_text, "", pasring_text.message, flags=re.DOTALL)

        # Удаление всех смайликов в тексте
        for i in emoji.UNICODE_EMOJI['en']:
            if i in pasring_text.message:
                pasring_text.message = pasring_text.message.replace(f"{i} ", "")
                break

    if event.grouped_id:
        return    # ignore messages that are gallery here
    await client.send_message(channel_PL, pasring_text)

# Копирует и пересылает фото не разделяя их на разные сообщения. Срабатывает, если фоток больше чем 1
@client.on(events.Album(chats=channel_from_pars))
async def parsing_almun(event):
    print("Сработал Album\n")
    await client.send_file(channel_PL, event.messages, caption=event.original_update.message.message)

client.start()
client.run_until_disconnected()
