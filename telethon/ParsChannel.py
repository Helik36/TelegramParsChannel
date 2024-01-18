import re

from Examples.tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL, CHANNEL_FROM_PARS
from notNeededWords import DELETE_TEXT
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

6. Допилить чтобы не было лишних \n

"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL
channel_from_pars = CHANNEL_FROM_PARS

# массив по которым будут удаляться ненужные слова или текст или вообще не выкладываться. Перенести в другой файл
delete_word = DELETE_TEXT


# Срабатывает на сообщения и на сообщения с фото 1.
@client.on(events.NewMessage(chats=channel_from_pars))
async def parsing_new_message(event):
    pasring_text = event.message
    # print(pasring_text.message) # Для дебага сообщений

    # Сделать отдельную функцию по отработке фильтров. Аля удаление слов, удаление текста. Не постить вообще
    # Удаляем теги, предложения (Если удаляется предложение, и с ним целый абзац). Нужно додумать, как удалять именно слова либо только 1 предложение
    for word in range(len(delete_word)):

        # Сделал двойную проверку. При первой проверке удаляется слово с пробелами. если их больше 1 после окончания текста.
        if delete_word[word] in pasring_text.message:
            pasring_text.message = pasring_text.message.replace(re.findall(fr"(.*?{delete_word[word]}.+\s+)", pasring_text.message)[0], "")
            # Но может быть такое, что проблем действительно только 1. Тогда если первой не прошёл, проходит вторая и удаляет лишний пробел после текста
            if delete_word[word] in pasring_text.message:
                pasring_text.message = pasring_text.message.replace(
                    re.findall(fr"(.*?{delete_word[word]}.+)", pasring_text.message)[0], "")


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