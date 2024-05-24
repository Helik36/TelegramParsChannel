"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

token = ""

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
        messages.append(res)

        # Ответ модели
        return res.content

    except:
        logging.info("Возникла проблема с gigashat")
        return text
