import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect("database\\test_base.db")


########################################################################################################################


# Создание объекта курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
)
""")

# Сохранение изменений
conn.commit()


########################################################################################################################


# Вставка одной записи
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
conn.commit()

# Вставка нескольких записей
data = [("Bob", 30), ("Charlie", 22), ("David", 40)]
cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", data)
conn.commit()


########################################################################################################################


# Выборка всех записей
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Выборка записей с условием
cursor.execute("SELECT * FROM users WHERE age=?", (25,))
rows = cursor.fetchall()
for row in rows:
    print(row)

# Выборка записей с указанием получения конкретных столбиков
cursor.execute("SELECT * FROM users")
for person in cursor.fetchall():
    print(f"\nperson: {person[1]} - {person[2]}")

""" Можно и так
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row[1], " ", row[2])
"""

########################################################################################################################

# Обновление записи
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))
conn.commit()

# Удаление записи
cursor.execute("DELETE FROM users WHERE name = ?", ("Bob",))
conn.commit()


conn.close()
