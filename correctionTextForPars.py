from database.actionWithDB import get_handle_hashtag, get_handle_smiles, get_from_db_delete_text
from additional_files.notNeededWords import upd_delete_text
from rewriting_text import requsts_in_giga_chat


import re
import emoji  # pip install emoji==1.7
import logging

logging.basicConfig(filename='logs/app.log',
            format="\n[%(asctime)s]: %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            level=logging.INFO)


async def correction_text(event_message):
    delete_word = await upd_delete_text()
    change_text = event_message
    text = await get_from_db_delete_text()


    # Удаляем теги, предложения (Если удаляется предложение, и с ним целый абзац). Нужно додумать, как удалять именно слова либо только 1 предложение.
    for word in range(len(delete_word)):

        if delete_word[word] in change_text.message:

            # Если фильтр находится между двумя другими предложениями и если фильтр находится после предложения и он являтся последним предложением
            try:
                change_text.message = change_text.message.replace(
                    re.findall(
                        fr"(?<=[?!.])\s{text[word]}.*?[?!.][^.|^.ru|^.store]?(?=\s|$)", change_text.message)[0], "")
            except IndexError:
                pass

            # Если предложение является самым первым и после него есть предложение или нет текста
            try:
                change_text.message = change_text.message.replace(re.findall(
                    fr"{text[word]}.*?[?!.][^.|^.ru^.store]?(?=\s|\n)\s|{text[word]}.*?[?!.][^.|^.ru^.store]?(?=\s|\n|$)",
                    change_text.message)[0], "")
            except IndexError:
                pass

            # Делает так, чтобы не было двойных пустых отступов.
            try:
                change_text.message = change_text.message.replace(re.findall(fr"\n\s\n", change_text.message)[0],
                                                                  "\n\n")
            except IndexError:
                pass

        # Удаление хэштегов. Управляется через БД через команду
    if await get_handle_hashtag() == int(1):
        for i in re.findall(fr"(#.+)", change_text.message):
            change_text.message = change_text.message.replace(i, "")

    # Удаление всех смайликов в тексте. Управляется через БД через команду
    if await get_handle_smiles() == int(1):
            # change_text.message = change_text.message.replace(f"{i} ", "")
            change_text.message = re.sub(r'[^\w\s]', '', change_text.message)  # Удаляем unicode символы (смайлики)
            # re.sub(r'[^\x00-\x7F]+', '', message) - на всякий

    # Отдаём сообщение gigaChat
    logging.info("Передача текста ГигаЧату\n")
    change_text.message = await requsts_in_giga_chat(change_text.message)

    return change_text
