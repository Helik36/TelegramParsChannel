import sqlite3


def createbase():
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
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
    conn.commit()


# Добавить текст в БД для удаления из поста
def append_delete_text():
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    # Добавить одно слово
    # cursor.execute("INSERT INTO delete_text (text_trigger) VALUES (?)", ("asda",))
    # conn.commit()

    data = ["#", "vk", "t.me", "Free Gaming"]
    for word in data:
        cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [word])  # можно ещё как (word, )
        conn.commit()

    data = ["дарим", "конкурс", "подпишись", "подписаться", "розыгрыш"]
    for word in data:
        cursor.execute("INSERT INTO DBstop_post (text_stop_post_trigger) VALUES (?)", [word])  # можно ещё как (word, )
        conn.commit()

    # cursor.execute("SELECT * FROM delete_text")
    # data = cursor.fetchall()
    # for word in data:
    #     print(word[1])

    # cursor.execute("DROP TABLE IF EXISTS delete_text")
    conn.close()


# Добавить текст в БД для удаления из поста
async def append_in_db_delete_text_from_cmd(text):
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}`  для удаления из поста - добавлен")

# Добавить фильтр в БД для стоп слова
async def append_in_db_stop_pots_from_cmd(text):
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO DBstop_post (text_stop_post_trigger) VALUES (?)", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}`  для стоп-пост - добавлен")

# Удалить из бд фильтр для удления из поста
async def delete_from_db_delete_text_from_cmd(text):
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM DBdelete_text WHERE text_trigger = ?", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}` удалён")


# Удалить из бд фильтр стоп-пост
async def delete_from_db_text_stop_post_from_cmd(text):
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM dbstop_post WHERE text_stop_post_trigger = ?", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}` Удалён")


# Показать фильтр для удаления текста из поста
async def get_from_db_delete_text():
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    get_text = [text[0] for text in cursor.execute("SELECT text_trigger FROM DBdelete_text")]

    conn.close()
    return get_text


# Показать фильтры по стоп-посту
async def get_from_db_stop_post_text():
    conn = sqlite3.connect('database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    get_text = [text[0] for text in cursor.execute("SELECT text_stop_post_trigger FROM dbstop_post")]

    conn.close()
    return get_text


if __name__ == "__main__":
    createbase()
    append_delete_text()
