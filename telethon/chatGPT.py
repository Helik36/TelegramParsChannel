from additional_files.tokens_telethon import TOKEN_VSE_GPT
import re
import openai


async def rewrite(my_text):
    openai.api_key = TOKEN_VSE_GPT
    openai.base_url = "https://api.vsegpt.ru:6070/v1/"

    # my_text = """
    # Он все правильно делает?
    # """

    prompt = (
        "Твоя задача - переписать весь текст лучшими словами и сделать его уникальным на естественном языке. Не бойся использовать сленг"
        "Если в моём тексте присутсвутют отступы, старайся их сохранить, чтобы визуально можно было разбить текст на разные составляющие."
        "Если текст не очень большой, т.е. от 2 до 7 слов, измени буквально 1-2 слова. "
        "Текст который нужно переписать:"
        ""
        f"{my_text}")

    messages = [{"role": "user", "content": prompt}]

    response_big = openai.chat.completions.create(
        model="anthropic/claude-instant-v1",
        messages=messages,
        temperature=0.7,
        n=1,
        max_tokens=int(len(prompt) * 1.5),
    )

    response = response_big.choices[0].message.content
    # print(response)
    text = "Response: " + response
    text = text.replace(re.findall(r'Response.+[\s]+', text)[0], "")

    # print(text)
    return text


# answer = rewrite()



# print(answer)
