import sqlite3
# asdads


conn = sqlite3.connect('database\\DBnotNeededWords.db') # Тут надо менять путь в зависимости от того, где запускаешь файл
cursor = conn.cursor()

def upd_delete_text():
    conn = sqlite3.connect('database\\DBnotNeededWords.db')  # Тут надо менять путь в зависимости от того, где запускаешь файл
    cursor = conn.cursor()

    DELETE_TEXT = [row[0] for row in cursor.execute("SELECT text_trigger FROM DBdelete_text")]
    conn.close()

    return DELETE_TEXT

STOP_POST = [row[0] for row in cursor.execute("SELECT text_stop_post_trigger FROM DBstop_post")]

conn.close()
# print(DELETE_TEXT)
# print(STOP_POST)


### старое ###
# DELETE_TEXT = ["#", "vk", "t.me", "Free Gaming."]

# STOP_POST = ["дарим", "конкурс", "подпишись", "подписаться", "розыгрыш"]

DELETE_TEXT_SPECIFIC_WORDS = []

if __name__ == "__main__":

    conn = sqlite3.connect('..\\database\\DBnotNeededWords.db')  # Тут надо менять путь в зависимости от того, где запускаешь файл
    cursor = conn.cursor()

    DELETE_TEXT = [row[0] for row in cursor.execute("SELECT text_trigger FROM DBdelete_text")]

    STOP_POST = [row[0] for row in cursor.execute("SELECT text_stop_post_trigger FROM DBstop_post")]

    conn.close()
    # print(DELETE_TEXT)
    # print(STOP_POST)

    ### старое ###
    # DELETE_TEXT = ["#", "vk", "t.me", "Free Gaming."]

    # STOP_POST = ["дарим", "конкурс", "подпишись", "подписаться", "розыгрыш"]

    DELETE_TEXT_SPECIFIC_WORDS = []
