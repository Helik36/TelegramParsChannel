from actionWithDB import append_delete_text_from_cmd, append_stop_pots_from_cmd, get_delete_text, get_stop_post_text, delete_from_db_delete_text_from_cmd, delete_from_db_text_stop_post_from_cmd

from additional_files.notNeededWords import upd_delete_text, STOP_POST
import telethon
import re
from telethon import TelegramClient, events
import emoji  # pip install emoji==1.7
import logging
import asyncio
import sqlite3

async def input_cmd():
    delete_word = upd_delete_text()
    await asyncio.sleep(3)


    print("""\nДобавить текст/слово на удаление из поста - /add_delete_text или /1
Добавить текст/слово для стоп-пост - /add_text_stop_post или /2
Посмотреть текущение добавленные триггеры на удаление - /get_delete_text или /3
Посмотреть текущие стоп-пост триггеры - /get_text_stop_post или /4
Удалить текст/слово на удаление из поста - /del_from_db_text или /5
Удалить текст/слово для стоп-пост - /del_text_stop_post или /6
    """)

    while True:
        user_input = await asyncio.to_thread(input, "Введи комманду: ")
        if user_input == "check":

            conn = sqlite3.connect("database\\DBnotNeededWords.db")
            cursor = conn.cursor()
            print("pass")

            cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [user_input])
            conn.commit()

            cursor.execute("SELECT * FROM DBdelete_text")
            data = cursor.fetchall()
            print(data)

            conn.close()

        # Добавить тексть в базу на удаление
        elif user_input == "/add_delete_text" or  user_input == "/1":

            user_input2 = await asyncio.to_thread(input, "Введите текст, который нужно убирать из поста: ")
            await append_delete_text_from_cmd(user_input2)

            delete_word = upd_delete_text() # нужно постоянно обновлять переменную или просто

            print(get_delete_text())
            print(upd_delete_text())

        # Добавить тексть в базу для стоп пост
        elif user_input == "/add_text_stop_post" or  user_input == "/2":

            user_input2 = await asyncio.to_thread(input, "Введите текст для стоп слова: ")
            await append_stop_pots_from_cmd(user_input2)

            delete_word = upd_delete_text() # нужно постоянно обновлять переменную или просто

        # Посмотреть текущие предложения на удаление
        elif user_input == "/del_from_db_text" or  user_input == "/3":

            print(f"Текущие фильтры для удаления {get_delete_text()}")

        # Посмотреть текущие предложения на удаление
        elif user_input == "/get_text_stop_post" or  user_input == "/4":

            print(f"Текущие фильтры для стоп-пост: {get_stop_post_text()}")

        # Удалить из БД триггер
        elif user_input == "/del_from_db_text" or  user_input == "/5":

            user_input2 = await asyncio.to_thread(input, "Что нужно удалить из базы: ")
            await delete_from_db_delete_text_from_cmd(user_input2)

            print(get_delete_text())

        # Удалить из БД триггер
        elif user_input == "/del_text_stop_post" or  user_input == "/6":

            user_input2 = await asyncio.to_thread(input, "Что нужно удалить из базы: ")
            await delete_from_db_text_stop_post_from_cmd(user_input2)

            print(get_delete_text())

        elif user_input == "exit":
            break

        else:
            print("""Некорректная команда
Добавить фильтр на удаление из поста - /add_delete_text или /1
Добавить фильтр для стоп-пост - /add_text_stop_post или /2
Посмотреть текущение фильтры на удаление - /get_delete_text или /3
Посмотреть текущие стоп-пост фильтры - /get_text_stop_post или /4
Удалить текст/слово на удаление из поста - /del_from_db_text или /5
Удалить текст/слово для стоп-пост - /del_text_stop_post или /6
        """)