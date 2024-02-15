import asyncio
import sqlite3


def createbase():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DBdelete_text (
        id INTEGER PRIMARY KEY,
        text_trigger TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DBstop_post (
        id INTEGER PRIMARY KEY,
        text_stop_post_trigger TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DBhandle_hashtag (
        handle_hashtag INTEGER
    )
    """)
    conn.commit()


# Добавить текст в БД для удаления из поста
def append_delete_text():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    # Добавить одно слово
    # cursor.execute("INSERT INTO delete_text (text_trigger) VALUES (?)", ("asda",))
    # conn.commit()

    data = ["Free Gaming", 'Если понадобится — создадим зарубежный аккаунт', 'Цены ниже указаны при покупке с нашей помощью']

    for word in data:
        cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [word])  # можно ещё как (word, )
        conn.commit()

    data = ["дарим", "конкурс", "подпишись", "розыгрыш"]
    for word in data:
        cursor.execute("INSERT INTO DBstop_post (text_stop_post_trigger) VALUES (?)", [word])  # можно ещё как (word, )
        conn.commit()

    cursor.execute("INSERT INTO DBhandle_hashtag (handle_hashtag) VALUES (?)", [1])
    conn.commit()

    # cursor.execute("SELECT * FROM delete_text")
    # data = cursor.fetchall()
    # for word in data:
    #     print(word[1])

    # cursor.execute("DROP TABLE IF EXISTS delete_text")
    conn.close()


# Добавить текст в БД для удаления из поста
async def append_in_db_delete_text_from_cmd(text):

    # Нужно, чтобы когда добавлятся текст со скобками, перед ним ставился слеш, иначе регулярка воспринимает как часть скрипта, а не текста
    replace_symbols = ["(", ")"]
    for symbol in replace_symbols:
        text = text.replace(f"{symbol}", f"\\{symbol}")

    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}`  для удаления из поста - добавлен")


# Добавить фильтр в БД для стоп слова
async def append_in_db_stop_pots_from_cmd(text):

    # Нужно, чтобы когда добавлятся текст со скобками, перед ним ставился слеш, иначе регулярка воспринимает как часть скрипта, а не текста
    replace_symbols = ["(", ")"]
    for symbol in replace_symbols:
        text = text.replace(f"{symbol}", f"\\{symbol}")

    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO DBstop_post (text_stop_post_trigger) VALUES (?)", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}`  для стоп-пост - добавлен")


# Удалить из бд фильтр для удления из поста
async def delete_from_db_delete_text_from_cmd(text):

    # Т.к ранее текст со скобками добавлялся со слешом, то и удалить его нужно со слешом
    replace_symbols = ["(", ")"]
    for symbol in replace_symbols:
        text = text.replace(f"{symbol}", f"\\{symbol}")

    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM DBdelete_text WHERE text_trigger = ?", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}` удалён")


# Удалить из бд фильтр стоп-пост
async def delete_from_db_text_stop_post_from_cmd(text):

    # Т.к ранее текст со скобками добавлялся со слешом, то и удалить его нужно со слешом
    replace_symbols = ["(", ")"]
    for symbol in replace_symbols:
        text = text.replace(f"{symbol}", f"\\{symbol}")

    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM dbstop_post WHERE text_stop_post_trigger = ?", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}` Удалён")


# Показать фильтр для удаления текста из поста
async def get_from_db_delete_text():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    get_text = [text[0] for text in cursor.execute("SELECT text_trigger FROM DBdelete_text")]
    conn.close()

    return get_text


# Показать фильтры по стоп-посту
async def get_from_db_stop_post_text():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    get_text = [text[0] for text in cursor.execute("SELECT text_stop_post_trigger FROM dbstop_post")]
    conn.close()

    return get_text


async def swith_handle_hashtag(value):
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE DBhandle_hashtag set handle_hashtag = ? ", [value])
    conn.commit()

    conn.close()

    return print(f"Переключён")


async def get_handle_hashtag():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    res = [text[0] for text in cursor.execute("SELECT * FROM DBhandle_hashtag")]
    conn.commit()

    conn.close()

    return res[0]


if __name__ == "__main__":
    # createbase()
    # append_delete_text()
    asyncio.run(swith_handle_hashtag(1))
    # print(asyncio.run(get_from_db_delete_text()))
