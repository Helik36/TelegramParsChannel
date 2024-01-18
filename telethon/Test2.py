import re

delete_text = ["#", "Предзаказать его можно с нашей помощью", "vk", "t.me"]

# Мысль - Если есть фраза "с нашей помощью" находить всю строку и удалять. Либо по ВК/t.me
# Потыкать регекс на Предзаказать его можно с нашей помощью. Пишите в сообщения группы ВК (https://vk.me/pswrld.store) или Telegram (https://t.me/pswrld_store)
text1 = """
В PlayStation Store появилась демо-версия Prince of Persia: The Lost Crown

В турецком регионе есть русские субтитры. 

Вместе с этим появились и первые оценки проекта. На Opencritic игре удалось набрать 88 баллов из 100. Также 97% журналистов рекомендуют тайтл к прохождению.

• Game Informer - 9.5/10 
• GameSpot - 9/10 
• Easy Allies - 9/10 
• Wccftech - 9/10 
• TheSixthAxis - 9/10 
• Nintendo Life - 9/10 
• Press Start - 9/10 
• IGN - 8/10 
• Push Square - 8/10 
• Videogamer - 8/10 
• VGC - 4/5 
• Window Central - 4/5

Релиз игры состоится уже 18 января на PS5, PS4, Xbox Series S|X, Xbox One, Nintendo Switch и PC. 

Приобрести игру можно с нашей помощью. Пишите нам в сообщения группы ВКонтакте (https://vk.me/pswrld.store) или Telegram (https://pswrld.ru/store). Если понадобится — создадим зарубежный аккаунт. 

#PSNews #PrinceOfPerisaTheLostCrown
https://youtu.be/FgDZYxGKxNo
"""

text2 = []
for text in range(len(delete_text)):
    if delete_text[text] in text1:
        text1 = text1.replace(re.findall(fr"(.+{delete_text[text]}.+\s+)", text1)[0], "")


print(text1)
