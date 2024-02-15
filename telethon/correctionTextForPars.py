from tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL, CHANNEL_FROM_PARS

from actionWithDB import get_handle_hashtag, get_from_db_delete_text

from additional_files.notNeededWords import upd_delete_text

import re
from telethon import TelegramClient
import emoji  # pip install emoji==1.7
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

"""
Мысли:

Заметил, что если если событие не срабатывает на канал, возможно это интегрированная реклама, которая была выложена 
не как пост, а именно как реклама. Скрипт не реагирует на тикие посты

upd - Такое ощущение, что это не всегда так. Иногда была вроде не реклама, но скрипт не ловил активность
"""

"""
Если буду продавать скрипт

1. Сделать несколько версий

1.1 Версия без chatGPT
1.2 Версия с chatGPT
1.3 Версия с доп. ботом, через которого можно настраивать различные параметры (фильтр слов/предложений)
1.4 Версия с доп. ботом + chatGPT, через которого можно настраивать различные параметры (фильтр слов/предложений + параметры chatGPT)
п.с Если будет доп.бот, то тогда база нужна по любому
"""

"""
Парсим сообщение. Переселываем в канал

Задачи:

1. Придумать задачи

2. Поправить фильтр. Сейчас если есть абзац и в нём 2 предложения, даже если 1, удаляются оба.

3. Обдумать добавление тегов

4. Обдумать добавление базы

5. Обдумать добавление взаимодействия с ботом, чтобы был как админ-панель

6. Добавить ручки включения/выключения - Удалить смайлики, удалить ссылки и т.п

7. Добавить чат бот-модератор

"""

"""
Решил отложить 

Взаимодействие с GPT. Добавить либо потом, когда закончу остальные задачи, либо вообще не добавлять.
Если буду добавлять, обдумать промт, траты токенов и вообще логику взаимодействия
"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL
channel_from_pars = CHANNEL_FROM_PARS

async def correction_text(event_message):
    delete_word = await upd_delete_text()
    change_text = event_message
    text = await get_from_db_delete_text()

    # Удаляем теги, предложения (Если удаляется предложение, и с ним целый абзац). Нужно додумать, как удалять именно слова либо только 1 предложение.
    for word in range(len(delete_word)):

        if delete_word[word] in change_text.message:

            # Если фильтр находится между двумя другими предложениями и если фильтр находится после предложения и он являтся последним предложением
            try:
                change_text.message = change_text.message.replace(
                    re.findall(
                        fr"(?<=[?!.])\s{text[word]}.*?[?!.][^.|^.ru|^.store]?(?=\s|$)", change_text.message)[0], "")
            except IndexError:
                pass

            # Если предложение является самым первым и после него есть текст или нет текста
            try:
                change_text.message = change_text.message.replace(re.findall(
                    fr"{text[word]}.*?[?!.][^.|^.ru^.store]?(?=\s|\n)\s|{text[word]}.*?[?!.][^.|^.ru^.store]?(?=\s|\n|$)",
                    change_text.message)[0], "")
            except IndexError:
                pass

            # Делает так, чтобы не было двойных пустых отступов.
            try:
                change_text.message = change_text.message.replace(re.findall(fr"\n\s\n", change_text.message)[0], "\n\n")
            except IndexError:
                pass

        # Удаление хэштегов
    if await get_handle_hashtag() == int(1):
        for i in re.findall(fr"(\n.*?#.+)", change_text.message):
            change_text.message = change_text.message.replace(i, "")

    # Удаление всех смайликов в тексте. Иногда смайлики могут пролетать т.к. разный регион
    for i in emoji.UNICODE_EMOJI['en']:
        if i in change_text.message:
            change_text.message = change_text.message.replace(f"{i} ", "")
            break

    return change_text