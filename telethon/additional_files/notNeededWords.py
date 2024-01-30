import sqlite3

def createbase():

    conn = sqlite3.connect('..\\database\\DBnotNeededWords.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delete_text (
        id INTEGER PRIMARY KEY,
        text_trigger TEXT NOT NULL
    )
    """)
    conn.commit()


    # Добавить одно слово
    # cursor.execute("INSERT INTO delete_text (text_trigger) VALUES (?)", ("asda",))
    # conn.commit()

    data = ["#", "vk", "t.me", "Free Gaming"]
    for word in data:
        cursor.execute("INSERT INTO delete_text (text_trigger) VALUES (?)", [word]) # можно ещё как (word, )
        conn.commit()

    cursor.execute("SELECT * FROM delete_text")
    data = cursor.fetchall()
    for word in data:
        print(word[1])

    # cursor.execute("DROP TABLE IF EXISTS delete_text")
    # conn.commit()
    conn.close()



### старое ###
DELETE_TEXT = ["#", "vk", "t.me", "Free Gaming."]

STOP_POST = ["дарим", "конкурс", "подпишись", "подписаться", "розыгрыш",]

DELETE_TEXT_SPECIFIC_WORDS = []

if __name__ == "__main__":
    createbase()
