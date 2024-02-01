import sqlite3
from additional_files.notNeededWords import DELETE_TEXT

conn = sqlite3.connect('database\\DBnotNeededWords.db')
cursor = conn.cursor()

var_mass = []

cursor.execute("SELECT text_trigger FROM delete_text")
result = cursor.fetchall()
for var in result:
    var_mass.append(var[0])
print(var_mass)
# Короткая запись - var_mass = [row[0] for row in cursor.fetchall()]


print(DELETE_TEXT)
