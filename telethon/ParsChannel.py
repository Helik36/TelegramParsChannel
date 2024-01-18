import re

from Examples.tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL, CHANNEL_FROM_PARS
from notNeededWords import DELETE_TEXT
from telethon import TelegramClient, events
import emoji

import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

"""
Парсим сообщение. Переселываем в канал

Задачи:

1. Придумать задачи

2. После получения события, забирать сообщение, немного изменять его (chatgpt), и отправлять

3. Обдумать добавление тегов

4. Поправить фильтр. Сейчас если есть абзац и в нём 2 предложения, даже если 1, удаляются оба.

"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL
channel_from_pars = CHANNEL_FROM_PARS

# массив по которым будут удаляться ненужные слова или текст или вообще не выкладываться. Перенести в другой файл
delete_word = DELETE_TEXT


def correction_text(event_message):
    pasring_text = event_message
    # Сделать отдельную функцию по отработке фильтров. Аля удаление слов, удаление текста. Не постить вообще
    # Удаляем теги, предложения (Если удаляется предложение, и с ним целый абзац). Нужно додумать, как удалять именно слова либо только 1 предложение
    for word in range(len(delete_word)):

        # Сделал двойную проверку.
        # При первой проверке удаляется слово с пробелами. если их больше 1 после окончания текста.
        if delete_word[word] in pasring_text.message:

            # Пытаемся получить массив из найденных слов
            try:
                pasring_text.message = pasring_text.message.replace(
                    re.findall(fr"(.*?{delete_word[word]}.+\s+)", pasring_text.message)[0], "")

        # Но может быть такое, что пробел действительно только 1.
        # Тогда если первой не прошёл, проходит вторая и удаляет лишний пробел после текста
                if delete_word[word] in pasring_text.message:
                    pasring_text.message = pasring_text.message.replace(
                        re.findall(fr"(.*?{delete_word[word]}.+)", pasring_text.message)[0], "")

            # Но если слово одно и массив не сформирован, ловим исключение и обрабатываем
            except:
                if delete_word[word] in pasring_text.message:
                    pasring_text.message = pasring_text.message.replace(
                        re.findall(fr"(.*?{delete_word[word]}.+)", pasring_text.message)[0], "")

    # print(pasring_text.message) # Для дебага сообщений

    # Удаление всех смайликов в тексте
    for i in emoji.UNICODE_EMOJI['en']:
        if i in pasring_text.message:
            pasring_text.message = pasring_text.message.replace(f"{i} ", "")
            break

    return pasring_text


# Срабатывает на сообщения и на сообщения с фото 1.
@client.on(events.NewMessage(chats=channel_from_pars))
async def parsing_new_message(event):
    for i in range(len(CHANNEL_FROM_PARS)):
        # hasattr() принимает два аргумента: объект и имя атрибута в виде строки. Функция возвращает True, если у объекта есть атрибут с указанным именем, и False в противном случае.
        if hasattr(event.message.peer_id, "channel_id"):
            if int(f"-100{event.message.peer_id.channel_id}") == CHANNEL_FROM_PARS[i]:
                if CHANNEL_FROM_PARS[i] == -1001201194408:
                    print("Событие для PS WORLD\n")
                    break
                if CHANNEL_FROM_PARS[i] == -1001778660986:
                    print("Событие для КБ. ИГРЫ\n")
                    break
                if CHANNEL_FROM_PARS[i] == -1001908326943:
                    print("Событие для Пекашечка\n")
                    break
                if CHANNEL_FROM_PARS[i] == -1001397640032:
                    print("Событие для Раздача игр\n")
                    break
                if CHANNEL_FROM_PARS[i] == -1001322001342:
                    print("Событие для InYourEyes\n")
                    break
                if CHANNEL_FROM_PARS[i] == -1002076831448:
                    print("Событие для test\n")
                    break

    pasring_text = correction_text(event.message)
    # print(pasring_text.message)  # Для дебага сообщений

    if event.grouped_id:
        return  # ignore messages that are gallery here
    await client.send_message(channel_PL, pasring_text)


# Копирует и пересылает фото не разделяя их на разные сообщения. Срабатывает, если фоток больше чем 1
@client.on(events.Album(chats=channel_from_pars))
async def parsing_almun(event):
    print("Сработал Album\n")

    # Если отправляется альбом, в первом объекте сообщения может не быть, делаем проверку
    if not event.original_update.message.message:
        await client.send_file(channel_PL, event.messages, caption=event.messages[-1].message)
    else:
        await client.send_file(channel_PL, event.messages, caption=event.original_update.message.message)

client.start()
client.run_until_disconnected()
