import re

replace_symbols = ["(", ")"]

var = []

# user_input = input(":::: ")

text = """Файтинг 
 
• Mortal Kombat 11 (PS4, PS5) — 400 ₽ — русские субтитры 
• Mortal Kombat 11 Ultimate Add-On Bundle (PS4, PS5) — 300 ₽ — русские субтитры 
 
Для покупки с нашей помощью пишите нам в сообщения группы ВКонтакте (https://vk.me/pswrld.store) или Telegram (https://pswrld.ru/store).

asdasdasd"""

print(text)

for i in replace_symbols:
    # user_input = user_input.replace(f"{i}", f"\\{i}")

    text = text.replace("Для покупки с нашей помощью пишите нам в сообщения группы ВКонтакте (https://vk.me/pswrld.store) или Telegram (https://pswrld.ru/store)", "")

print(text)



