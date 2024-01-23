import re

text = """Here is a rewritten version of the text with a couple changes:

Новый день — новый рекорд: Palworld обогнала Dota 2 по пиковому онлайну за всю историю Steam  

Одновременно в игре находилось 1.854 миллиона игроков. Тем самым выживач с боевыми покемонами обогнал Dota 2 и занял вторую позицию в топе.

На пьедестале восседает PUBG: BATTLEGROUNDS c рекордом в 3.256 миллиона пользователей. Однако с таким темпом набора аудитории Palworld может сместить королевскую битву."""


# text = text.replace(re.findall(r'Response.+[\s]+', text)[0], "")

# try:
#     text = text.replace(re.findall(r"[\w].+:\n\n", text)[0], "")
#     print(text)
# except:
#     print(text)

if text != "":
    print(text)
else:
    print(text != "")
