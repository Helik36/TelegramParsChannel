from datetime import datetime
import sqlite3

# Для себя, чтобы не создавать опять всякое

def createbase():
    conn = sqlite3.connect('../database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY,
        id_channel INTEGER,
        name_channel TEXT NOT NULL
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DBhandle_smiles (
        handle_smiles INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_pause_for_post (
        id INTEGER PRIMARY KEY,
        time_end_pause_post TEXT NOT NULL
    )
    """)

    conn.commit()

    cursor.execute("INSERT INTO time_pause_for_post (time_end_pause_post) VALUES (?)", [str(datetime.now())])

    conn.commit()
    conn.close()


# Добавить текст в БД для удаления из поста
def append_delete_text():
    conn = sqlite3.connect('../database/DBnotNeededWords.db')
    cursor = conn.cursor()

    NAMES_CHANNEL = {-1002076831448: "Test",
                     -1001201194408: "PS WORLD",
                     -1001778660986: "КБ. ИГРЫ",
                     -1001908326943: "Пекашечка",
                     -1001397640032: "Раздача игр",
                     -1001322001342: "InYourEyes"}

    for i, j in NAMES_CHANNEL.items():
        cursor.execute("INSERT INTO channels (id_channel, name_channel) VALUES (?, ?)",
                       [i, j])
        conn.commit()

    data = ["Free Gaming", 'Если понадобится — создадим зарубежный аккаунт',
            'Цены ниже указаны при покупке с нашей помощью']
    for word in data:
        cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [word])  # можно ещё как (word, )
        conn.commit()

    data = ["дарим", "конкурс", "подпишись", "розыгрыш"]
    for word in data:
        cursor.execute("INSERT INTO DBstop_post (text_stop_post_trigger) VALUES (?)", [word])
        conn.commit()

    cursor.execute("INSERT INTO DBhandle_hashtag (handle_hashtag) VALUES (?)", [1])
    conn.commit()

    cursor.execute("INSERT INTO DBhandle_smiles (handle_smiles) VALUES (?)", [1])
    conn.commit()

    conn.close()

if __name__ == "__main__":

    conn = sqlite3.connect('../database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS time_pause_for_post (
         id INTEGER PRIMARY KEY,
         time_end_pause_post TEXT NOT NULL
     )
     """)

    conn.commit()

    cursor.execute("INSERT INTO time_pause_for_post (time_end_pause_post) VALUES (?)", [str(datetime.now())])

    conn.commit()
    conn.close()