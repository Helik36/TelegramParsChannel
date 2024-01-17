import re

delete_text = ["#", "Для покупки с нашей помощью", "Цена в рублях указана при покупке с нашей помощью", "vk", "t.me"]

# Мысль - Если есть фраза "с нашей помощью" находить всю строку и удалять. Либо по ВК/t.me
# Потыкать регекс на Предзаказать его можно с нашей помощью. Пишите в сообщения группы ВК (https://vk.me/pswrld.store) или Telegram (https://t.me/pswrld_store)
text1 = ("Critics Choice Awards прошла этой ночью — её триумфаторами стали «Оппенгеймер», «Барби», «Грызня» и «Медведь». "
         "\n\n"
         "Отдельно об итогах можно узнать в этой [https://vk.com/123123123123|заметке]."
         "\n\n"
         "Другие новости киноиндустрии: ")

text2 = []
for text in range(len(delete_text)):
    if delete_text[text] in text1:
        text2 = re.findall(fr"(.*?{delete_text[text]}.+)", text1)


for i in range(len(text2)):
    text1 = text1.replace(text2[i], "")


print(text1)
