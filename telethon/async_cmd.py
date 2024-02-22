from actionWithDB import (append_in_db_delete_text_from_cmd, append_in_db_stop_pots_from_cmd,
                          delete_from_db_delete_text_from_cmd, delete_from_db_text_stop_post_from_cmd,
                          switch_handle_hashtag, switch_handle_smiles, append_in_db_parschannel,
                          get_from_db_parschannel, del_from_db_parschannel)

from additional_files.notNeededWords import upd_delete_text, upd_stop_post

import asyncio



async def input_cmd():
    await asyncio.sleep(3)

    print("> Действие с каналами - /1\n> Действие с фильтрами - /2\n> Действие с тэгами, смайлами - /3\n")


    while True:
        user_input = await asyncio.to_thread(input, "Введи комманду: ")

        # Действие с каналами
        if user_input == "/1":

            print("\n> Посмотреть текущие каналы - /1\n> Добавить канал - /2\n> Удалить канал - /3\n< Назад - /4\n")

            user_input2 = await asyncio.to_thread(input, "Выберете действие: ")

            if user_input2 == "/1":
                channels = await get_from_db_parschannel()
                text = ""

                count = 1
                for i, j in channels.items():
                    text += f"{count}) {i} : {j}\n"
                    count += 1
                print(text)

            elif user_input2 == "/2":
                user_input3 = await asyncio.to_thread(input, "(//q - отмена действия) Укажите id и название канала через запятую: ")
                if user_input3 == "//q":
                    print("Отмена\n")
                else:
                    try:
                        await append_in_db_parschannel(user_input3)
                    except:
                        print("Неверно указан формат!! Укажите id и название канала через запятую")

            elif user_input2 == "/3":
                user_input3 = await asyncio.to_thread(input, "(//q - отмена действия) Введите название канала, который нужно удалить: ")
                if user_input3 == "//q":
                    print("Отмена\n")
                else:
                    await del_from_db_parschannel(user_input3)

            elif user_input2 == "/4":
                print("\n> Действие с каналами - /1\n> Действие с фильтрами - /2\n> Действие с тэгами, смайлами - /3\n")


        # Действие с фильтрами
        elif user_input == "/2":

            print("\n>> Действие с триггерами по удалению текста из поста - /1\n>> Действие с триггерами для стоп-пост - /2\n<< Назад - /3\n")
            user_input2 = await asyncio.to_thread(input, "Выберете действие: ")

            # >> Действие с триггерами по удалению текста из поста
            if user_input2 == "/1":

                print("\n>>> Посмотреть триггеры для удаления из поста - /1\n>>> Добавить триггер для удаления из поста - /2\n>>> Удалить триггер для удаления из поста - /3\n<<< Назад - /4\n")

                user_input3 = await asyncio.to_thread(input, "Выберете действие: ")

                if user_input3 == "/1":
                    rows = ""
                    text = [text for text in await upd_delete_text()]
                    for i in range(len(text)):
                        rows = rows + f"{i + 1}) {text[i]}\n"

                    print(f"\nТекущие триггеры для удаления:\n{rows}")

                elif user_input3 == "/2":
                    user_input4 = await asyncio.to_thread(input, "(//q - отмена действия)Внимание! Текст необходимо добавлять без точки в конце\nВведите текст, который нужно убирать из поста: ")

                    if user_input4 == "//q":
                        print("Отмена\n")
                    else:
                        await append_in_db_delete_text_from_cmd(user_input4)
                        print(await upd_delete_text())

                elif user_input3 == "/3":
                    rows = ""
                    check = [text for text in await upd_delete_text()]
                    for i in range(len(check)):
                        rows = rows + f"{i + 1}) {check[i]}\n"

                    user_input4 = await asyncio.to_thread(input, f"\n{rows}//q - отмена действия) Что нужно удалить из базы: ")

                    if user_input4 == "//q":
                        print("Отмена\n")
                    elif user_input4 in check:
                        await delete_from_db_delete_text_from_cmd(user_input4)
                        print(f"`{user_input4}` - удалён.")
                        print(await upd_delete_text())
                    else:
                        print("\nФильтр отсутствует!")
                        print(await upd_delete_text())



                elif user_input3 == "/4":
                    print("\n> Действие с каналами - /1\n> Действие с фильтрами - /2\n> Действие с тэгами, смайлами - /3\n")

            # >> Действия с триггерами стоп-пост
            elif user_input2 == "/2":
                print("\n>>> Посмотреть триггеры для стоп-пост - /1\n>>> Добавить триггер для стоп-пост - /2\n>>> Удалить триггер для стоп-пост - /3\n<<< Назад - /4\n")

                user_input3 = await asyncio.to_thread(input, "Выберете действие: ")

                if user_input3 == "/1":
                    rows = ""
                    text = [text for text in await upd_stop_post()]
                    for i in range(len(text)):
                        rows = rows + f"{i + 1}) {text[i]}\n"

                    print(f"Текущие триггеры для стоп-пост:\n{rows}")

                elif user_input3 == "/2":

                    user_input4 = await asyncio.to_thread(input, "(//q - отмена действия)Внимание! Текст необходимо добавлять без точки в конце\nВведите текст для стоп слова: ")
                    if user_input4 == "//q":
                        print("Отмена\n")
                    else:
                        await append_in_db_stop_pots_from_cmd(user_input4)
                        print(await upd_stop_post())

                elif user_input3 == "/3":
                    rows = ""
                    check = [text for text in await upd_stop_post()]
                    for i in range(len(check)):
                        rows = rows + f"{i + 1}) {check[i]}\n"

                    user_input4 = await asyncio.to_thread(input, f"\n{rows}(//q - отмена действия) Что нужно удалить из базы: ")

                    if user_input4 == "//q":
                        print("Отмена\n")
                    elif user_input4 in check:
                        await delete_from_db_text_stop_post_from_cmd(user_input4)
                        print(f"`{user_input4}` - удалён.")
                    else:
                        print("\nФильтр отсутствует!")

                    print(await upd_stop_post())

                elif user_input3 == "/4":
                    print("\n> Действие с каналами - /1\n> Действие с фильтрами - /2\n> Действие с тэгами, смайлами - /3\n")

        # >> Действие с хэштегами, смайлами
        elif user_input == "/3":

            print("\n>> Действия с удалением хэштегов - /1\n>> Действий с удалением смайлов - /2\n<< Назад - /3\n")

            user_input2 = await asyncio.to_thread(input, "Выберете действие: ")

            if user_input2 == "/1":

                user_input3 = await asyncio.to_thread(input, "Удаление хэштегов:\n  1 - Включить\n  0 - выключить:\n ")
                if user_input3 == '1':
                    await switch_handle_hashtag(int(user_input3))
                elif user_input3 == "0":
                    await switch_handle_hashtag(int(user_input3))

            elif user_input2 == "/2":
                user_input3 = await asyncio.to_thread(input, "Удаление смайлов:\n   1 - Включить\n   0 - Выключить:\n ")
                if user_input3 == '1':
                    await switch_handle_smiles(int(user_input3))
                elif user_input3 == "0":
                    await switch_handle_smiles(int(user_input3))

            elif user_input2 == "/3":
                print("\n> Действие с каналами - /1\n> Действие с фильтрами - /2\n> Действие с тэгами, смайлами - /3\n")

        else:
            print("\nНекорректная команда\n> Действие с каналами - /1\n> Действие с фильтрами - /2\n> Действие с тэгами, смайлами - /3 \n")


