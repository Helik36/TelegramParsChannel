"""Пример работы с чатом через gigachain"""
import os

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from tokens.tokens import TOKEN_GIGA_CHAT
import logging

try:
    os.mkdir("logs")
except FileExistsError:
    pass

logging.basicConfig(filename='logs/app.log',
            format="\n[%(asctime)s]: %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            level=logging.INFO)

token = TOKEN_GIGA_CHAT

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=token, verify_ssl_certs=False)


async def requsts_in_giga_chat(text):
    messages = [
        SystemMessage(
            content="Ты профессиональный бот рерайтер. Измени текст, сохраняя смысл и отступы"
        )
    ]

    # Ввод текста
    user_input = f"""{text}"""

    messages.append(HumanMessage(content=user_input))

    try:
        res = chat(messages)

        try:
            os.mkdir("rewrite_file")
            with open("rewrite_file/rewrtire_text.txt", "a") as file:
                file.write(f"{res.content}\n\n")

        except:
            with open("rewrite_file/rewrtire_text.txt", "a") as file:
                file.write(f"{res.content}\n\n")

        messages.append(res)

        # Ответ модели
        logging.info("Текст успешно переделан\n")
        return res.content

    except Exception as e:
        logging.error("Возникла проблема с gigashat", e, exc_info=True)
        return text
