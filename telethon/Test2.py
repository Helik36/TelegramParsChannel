import re

delete_text = ["#", "Предзаказать его можно с нашей помощью", "vk", "t.me"]

# Мысль - Если есть фраза "с нашей помощью" находить всю строку и удалять. Либо по ВК/t.me
# Потыкать регекс на Предзаказать его можно с нашей помощью. Пишите в сообщения группы ВК (https://vk.me/pswrld.store) или Telegram (https://t.me/pswrld_store)
text1 = """
Hangar 13  анонсировала (https://youtu.be/8RGxSiweoJA) TopSpin 2K25 — первую новую игру в серии симуляторов тенниса за последние 13 лет. 

Анонс неожиданно подтвердил информацию Kotaku, опубликованная весной 2022 года. Подтверждение первой части инсайда придает весу второй, которая касается Mafia 4.

#игры
"""

text2 = []
for text in range(len(delete_text)):
    if delete_text[text] in text1:
        # print(re.findall(fr"(.*?{delete_text[text]}.+)", text1)[0])
        try:
            text1.replace(re.findall(fr"(.*?{delete_text[text]}.+\s+)", text1)[0])
        except:
            print(re.findall(fr"(.*?{delete_text[text]}.+)", text1)[0])


# print(text1)
