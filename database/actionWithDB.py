import sqlite3
from datetime import datetime


# Действие с каналами
async def append_in_db_parschannel(channnel):
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    get_id_name = channnel.split(", ")

    channnel = {get_id_name[0]: get_id_name[1]}

    for i, j in channnel.items():
        cursor.execute("INSERT INTO channels (id_channel, name_channel) VALUES (?, ?)",
                       [i, j])
        conn.commit()
        conn.close()

        return print(f"Канал `{channnel[i]}` - добавлен")


async def db_get_id_parschannel():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    CHANNEL_FROM_PARS = [i[0] for i in cursor.execute("SELECT id_channel from channels")]

    return CHANNEL_FROM_PARS


async def get_from_db_parschannel():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    names_channel = {}
    for i, j in cursor.execute("SELECT id_channel, name_channel from channels"):
        names_channel[i] = j
    conn.close()

    return names_channel


async def del_from_db_parschannel(channnel):
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM channels WHERE name_channel = ?", [channnel])

    conn.commit()
    conn.close()

    return print(f"Канал `{channnel}` - удалён")

# Действия со своими каналами

async def get_my_id_channel():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    channel = [i[0] for i in cursor.execute("SELECT id_channel from my_channels")]

    return channel

async def get_from_db_my_channel():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    names_channel = {}
    for i, j in cursor.execute("SELECT id_channel, name_channel from my_channels"):
        names_channel[i] = j
    conn.close()

    return names_channel


async def add_my_channel(my_channnel):
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    get_id_name = my_channnel.split(", ")

    channnel = {get_id_name[0]: get_id_name[1]}

    for i, j in channnel.items():
        cursor.execute("INSERT INTO my_channels (id_channel, name_channel) VALUES (?, ?)",
                       [i, j])
        conn.commit()
        conn.close()

        return print(f"Канал `{channnel[i]}` - добавлен")


async def del_from_db_my_channel(channnel):
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM my_channels WHERE name_channel = ?", [channnel])

    conn.commit()
    conn.close()

    return print(f"Канал `{channnel}` - удалён")


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


# Показать фильтр для удаления текста из поста
async def get_from_db_delete_text():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    get_text = [text[0] for text in cursor.execute("SELECT text_trigger FROM DBdelete_text")]
    conn.close()

    return get_text


# Удалить из бд фильтр для удаления из поста
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


# Показать фильтры по стоп-посту
async def get_from_db_stop_post_text():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    get_text = [text[0] for text in cursor.execute("SELECT text_stop_post_trigger FROM DBstop_post")]
    conn.close()

    return get_text


# Удалить из бд фильтр стоп-пост
async def delete_from_db_text_stop_post_from_cmd(text):
    # Т.к ранее текст со скобками добавлялся со слешом, то и удалить его нужно со слешом
    replace_symbols = ["(", ")"]
    for symbol in replace_symbols:
        text = text.replace(f"{symbol}", f"\\{symbol}")

    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM DBstop_post WHERE text_stop_post_trigger = ?", [text])
    conn.commit()

    conn.close()
    return print(f"Фильтр `{text}` Удалён")


async def switch_handle_hashtag(value):
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


async def switch_handle_smiles(value):
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE DBhandle_smiles set handle_smiles = ? ", [value])
    conn.commit()
    conn.close()

    return print(f"Переключён")


async def get_handle_smiles():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    res = [text[0] for text in cursor.execute("SELECT * FROM DBhandle_smiles")]
    conn.commit()
    conn.close()

    return res[0]


def create_table_time_pause_post():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
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

async def get_time_pause_post():
    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    res = [text[0] for text in cursor.execute("SELECT time_end_pause_post FROM time_pause_for_post")]

    return res[0]

async def set_new_time_pause_post(time):

    conn = sqlite3.connect('database/DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE time_pause_for_post set time_end_pause_post = ? ", [time])

    conn.commit()
    conn.close()

