from actionWithDB import (append_in_db_delete_text_from_cmd, append_in_db_stop_pots_from_cmd,
                          delete_from_db_delete_text_from_cmd, delete_from_db_text_stop_post_from_cmd, swith_handle_hashtag)

from additional_files.notNeededWords import upd_delete_text, upd_stop_post

import asyncio
import sqlite3


async def input_cmd():
    await asyncio.sleep(3)

    print("""\n
    Добавить текст/слово на удаление из поста - /add_delete_text или /1
Добавить текст/слово для стоп-пост - /add_text_stop_post или /2
Посмотреть текущение добавленные триггеры на удаление - /get_delete_text или /3
Посмотреть текущие стоп-пост триггеры - /get_text_stop_post или /4
Удалить текст/слово на удаление из поста - /del_from_db_text или /5
Удалить текст/слово для стоп-пост - /del_text_stop_post или /6
Включить/Выключить (1/0) удаление тэгов: 1/0 - /switch_hashtag или /7

Текст необходимо добавлять без точки на конце
    \n""")

    while True:
        user_input = await asyncio.to_thread(input, "Введи комманду: ")
        if user_input == "check":

            conn = sqlite3.connect("database/DBnotNeededWords.db")
            cursor = conn.cursor()
            print("pass")

            cursor.execute("INSERT INTO DBdelete_text (text_trigger) VALUES (?)", [user_input])
            conn.commit()

            cursor.execute("SELECT * FROM DBdelete_text")
            data = cursor.fetchall()
            print(data)

            conn.close()

        # Добавить тексть в базу на удаление
        elif user_input == "/add_delete_text" or user_input == "/1":

            user_input2 = await asyncio.to_thread(input, "Введите текст, который нужно убирать из поста: ")
            await append_in_db_delete_text_from_cmd(user_input2)
            print(await upd_delete_text())

        # Добавить тексть в базу для стоп пост
        elif user_input == "/add_text_stop_post" or user_input == "/2":

            user_input2 = await asyncio.to_thread(input, "Введите текст для стоп слова: ")
            await append_in_db_stop_pots_from_cmd(user_input2)
            print(await upd_stop_post())

        # Посмотреть текущие предложения на удаление
        elif user_input == "/del_from_db_text" or user_input == "/3":
            print(f"Текущие фильтры для удаления {await upd_delete_text()}")

        # Посмотреть текущие предложения на удаление
        elif user_input == "/get_text_stop_post" or user_input == "/4":
            print(f"Текущие фильтры для стоп-пост: {await upd_stop_post()}")

        # Удалить из БД триггер
        elif user_input == "/del_from_db_text" or user_input == "/5":

            user_input2 = await asyncio.to_thread(input, "Что нужно удалить из базы: ")
            await delete_from_db_delete_text_from_cmd(user_input2)
            print(await upd_delete_text())

        # Удалить из БД триггер
        elif user_input == "/del_text_stop_post" or user_input == "/6":

            user_input2 = await asyncio.to_thread(input, "Что нужно удалить из базы: ")
            await delete_from_db_text_stop_post_from_cmd(user_input2)

            print(await upd_stop_post())

        elif user_input == "/switch_hashtag" or user_input == "/7":

            user_input2 = await asyncio.to_thread(input, "1 - Включить\n0 - выключить:\n ")
            if user_input2 == '1':
                await swith_handle_hashtag(int(user_input2))
            elif user_input2 == "0":
                await swith_handle_hashtag(int(user_input2))

        else:
            print("""Некорректная команда
Добавить фильтр на удаление из поста - /add_delete_text или /1
Добавить фильтр для стоп-пост - /add_text_stop_post или /2
Посмотреть текущение фильтры на удаление - /get_delete_text или /3
Посмотреть текущие стоп-пост фильтры - /get_text_stop_post или /4
Удалить текст/слово на удаление из поста - /del_from_db_text или /5
Удалить текст/слово для стоп-пост - /del_text_stop_post или /6
Включить/Выключить (1/0) удаление тэгов: 1/0 - /switch_hashtag или /7
        """)
