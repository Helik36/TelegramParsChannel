from additional_files.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL, CHANNEL_FROM_PARS, NAMES_CHANNEL
from additional_files.notNeededWords import DELETE_TEXT, STOP_POST
from chatGPT import rewrite
import telethon
import re
from telethon import TelegramClient, events
import emoji #  pip install emoji==1.7
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

2. После получения события, забирать сообщение, немного изменять его (chatgpt), и отправлять
upd: для chatgpt нужны токены чтобы использовать API. Подумать или найти другие варианты

3. Обдумать добавление тегов

4. Поправить фильтр. Сейчас если есть абзац и в нём 2 предложения, даже если 1, удаляются оба.
4.1. Фильтр, по котором пост вообще не будет выкладываться

5. Обдумать добавление базы

6. Обдумать добавление взаимодействия с ботом, чтобы был как админ-панель

7. Добавить ручки включения/выключения - Удалить смайлики, удалить ссылки и т.п

"""

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL
channel_from_pars = CHANNEL_FROM_PARS

# Массив по которым будут удаляться ненужные слова или текст или вообще не выкладываться. Перенести в другой файл
delete_word = DELETE_TEXT


def correction_text(event_message):

    change_text = event_message

    # Сделать отдельную функцию по отработке фильтров. Аля удаление слов, удаление текста. Не постить вообще
    # Удаляем теги, предложения (Если удаляется предложение, и с ним целый абзац). Нужно додумать, как удалять именно слова либо только 1 предложение
    for word in range(len(delete_word)):

        # 1.1 Сделал двойную проверку.
        # 1.2 При первой проверке удаляется слово с пробелами. Если их больше 1 после окончания текста.
        if delete_word[word] in change_text.message:

            # 2.1 Пытаемся получить массив из найденных слов
            try:
                change_text.message = change_text.message.replace(
                    re.findall(fr"(.*?{delete_word[word]}.+\s+)", change_text.message)[0], "")

                # 1.3 Но может быть такое, что пробел действительно только 1.
                # 1.4 Тогда если первой не прошёл, проходит вторая и удаляет лишний пробел после текста
                if delete_word[word] in change_text.message:
                    change_text.message = change_text.message.replace(
                        re.findall(fr"(.*?{delete_word[word]}.+)", change_text.message)[0], "")

            # 2.2 Но если слово одно и массив не сформирован, ловим исключение и обрабатываем
            except:
                if delete_word[word] in change_text.message:
                    change_text.message = change_text.message.replace(
                        re.findall(fr"(.*?{delete_word[word]}.+)", change_text.message)[0], "")

    # print(pasring_text.message) # Для дебага сообщений

    # Удаление всех смайликов в тексте. Иногда смайлики могут пролетать т.к. разный регион
    for i in emoji.UNICODE_EMOJI['en']:
        if i in change_text.message:
            change_text.message = change_text.message.replace(f"{i} ", "")
            break

    return change_text

# Срабатывает на сообщения и на сообщения с фото 1.
@client.on(events.NewMessage(chats=channel_from_pars))
async def parsing_new_message(event):

    print(event.message) # Дебаг
    print(event.message.message)  # Дебаг

    # Дебаг, на какой канал сработало событие
    # hasattr() принимает два аргумента: объект и имя атрибута в виде строки.
    # Функция возвращает True, если у объекта есть атрибут с указанным именем, и False в противном случае.
    if event.message.message != "":
        if hasattr(event.message.peer_id, "channel_id"):
            if int(f"-100{event.message.peer_id.channel_id}") in list(NAMES_CHANNEL):
                print(NAMES_CHANNEL[int(f"-100{event.message.peer_id.channel_id}")]) # Тут словарь

    pasring_text = event.message
    pasring_text = correction_text(pasring_text)

    # print(pasring_text.message)   # Дебаг

    # Обращение к GPT
    if 5 < len(pasring_text.message) < 1024:
        pasring_text.message = await rewrite(pasring_text.message)

    if event.grouped_id:
        return  # ignore messages that are gallery here

    # Пояснение зачем тут try except:
    # По умолчанию, если отправляется фотка, к ней можно приложить текст с не более 1024 символов. Иначе будет ошибка
    # Решение: 1) Чтобы этого избежать, нужен премиум, он даёт 20248 символов. 2) Либо отправлять картинку как ссылку
    # Если текста нет вообще, сообщение может не отправиться. Проверить и подумать
    try:
        await client.send_message(channel_PL, pasring_text)
    except telethon.errors.rpcerrorlist.MediaCaptionTooLongError:
        print("В тексте больше 1024 символов. Пост игнорируется")


# Копирует и пересылает фото не разделяя их на разные сообщения. Срабатывает, если фоток больше чем 1
@client.on(events.Album(chats=channel_from_pars))
async def parsing_almun(event):
    # print("Сработал Album\n")

    # Если отправляется альбом, в первом объекте текста может не быть, делаем проверку
    if not event.original_update.message.message:
        caption = event.messages[-1].message
        await client.send_file(channel_PL, event.messages, caption=caption)
    else:
        caption = event.original_update.message.message
        await client.send_file(channel_PL, event.messages, caption=caption)


client.start()
client.run_until_disconnected()
