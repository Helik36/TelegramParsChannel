import asyncio

from additional_files.tokens_telethon import TOKEN_VSE_GPT
import re
import openai


async def rewrite(my_text):
    openai.api_key = TOKEN_VSE_GPT
    openai.base_url = "https://api.vsegpt.ru:6070/v1/"

    # prompt = (
    #     "Your task is a rewrite of the text, just a couple of changes.Style is a news post in the Telegram channel."
    #     "If there is not enough text, replace just a couple of words. If there is a lot of text, then whole sentences can be used."
    #     "If there are indents in my text, try to keep them so that you can visually break the text into different components."
    #     "The text that needs to be rewritten:"
    #     ""
    #     f"{my_text}")

    prompt = (
        "Твоя задача -  небольшой рерайт текста, буквально пару изменений. Стиль - новостной пост в Телеграмм канале."
        # "Если текста мало, замени буквально пару слов. Если текста очень много, то можно целые предложенения."
        "Если в тексте присутсвутют отступы, старайся их сохранить, чтобы визуально можно было разбить текст на разные составляющие."
        "Текст который нужно переписать:"
        ""
        f"{my_text}")

    messages = [{"role": "user", "content": prompt}]

    response_big = openai.chat.completions.create(
        model="anthropic/claude-instant-v1",
        messages=messages,
        # Чем больше «temperature», тем более художественный даст ответ.
        # Чем меньше значение, тем более «скучным» или наукообразным будет ответ.
        temperature=0.5,
        n=1,
        max_tokens=int(len(prompt)),
    )

    response = response_big.choices[0].message.content
    # print(response)
    text = response

    try:
        text = text.replace(re.findall(r"[\w].+:\n\n", text)[0], "")
    except:
        pass

    # print(text)
    return text


if __name__ == "__main__":
    text = """Вышли обзоры GeForce RTX 4070 Ti Super

    Видеокарта оказалась всего на 7% быстрее обычной RTX 4070 Ti, а обойдется новинка $799"""

    answer = asyncio.run(rewrite(text))
    print(answer)
