from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
import asyncio
import logging

from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID
from additional_files.notNeededWords import upd_delete_text, upd_stop_post

from actionWithBot import hundler_add_filter_delete_text, hundler_add_filter_stop_post, \
    hundler_delete_filter_delete_text, hundler_delete_filter_stop_post, handle_switch_handle_hashtag_bot, handle_switch_handle_smiles_bot

from ParsChannel import start_bot
from async_cmd import input_cmd

token_bot = TOKEN
my_id = MY_ID
my_channel_id = MY_CHANNEL_ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

id_channel_pasring = ID_CHANNEL_ID

BUTTON, BACK, ADD_TEXT, ADD_STOP_POST, DELETE_TEXT, DELETE_STOP_POST, CHECK_TEXT, CHECK_STOP_POST, SWITHC_HANDLE_HASHTAG, SWITHC_HANDLE_SMILES = range(10)

"""
Две нижние функции нужны, чтобы вместо меню, которое делает FatherBot, можно было сделать самому
красивое и изменяемое сообщение, которое выводит бот.
"""


async def button(update, _):
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном случае могут возникнуть проблемы.
    await query.answer()

    if variant == "ADD_TEXT":
        await query.edit_message_text("Напиши текст, который нужно добвить как фильтр для удаления из поста")
        return ADD_TEXT

    elif variant == "ADD_STOP_POST":
        await query.edit_message_text("Напиши текст, который нужно добвить как фильтр для стоп-пост")
        return ADD_STOP_POST

    elif variant == "CHECK_TEXT":
        reply_message = ""
        text = [text for text in await upd_delete_text()]

        for i in range(len(text)):
            reply_message += f"{i + 1}) {text[i]}\n"

        keyboard = [[InlineKeyboardButton("<< назад", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Триггеры для удаления текста:\n\n{reply_message}", reply_markup=menu_markup)
        return BACK

    elif variant == "CHECK_STOP_POST":
        reply_message = ""
        text = [text for text in await upd_stop_post()]

        for i in range(len(text)):
            reply_message += f"{i + 1}) {text[i]}\n"

        keyboard = [[InlineKeyboardButton("<< назад", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Триггеры стоп-пост:\n\n{reply_message}", reply_markup=menu_markup)
        return BACK

    elif variant == "DELETE_TEXT":
        reply_message = ""
        text = [text for text in await upd_delete_text()]

        for i in range(len(text)):
            reply_message += f"{i + 1}) {text[i]}\n"

        await query.edit_message_text(f"Напиши фильтр удаления из поста который нужно убрать из БД:\n\n{reply_message}")
        return DELETE_TEXT

    elif variant == "DELETE_STOP_POST":
        reply_message = ""
        text = [text for text in await upd_stop_post()]

        for i in range(len(text)):
            reply_message += f"{i + 1}) {text[i]}\n"

        await query.edit_message_text(f"Напиши фильтр стоп-пост который нужно убрать из БД:\n\n{reply_message}")
        return DELETE_STOP_POST

    elif variant == "SWITHC_HANDLE_HASHTAG":

        keyboard = [[InlineKeyboardButton("Включить", callback_data='1')],
                    [InlineKeyboardButton("Выключить", callback_data='0')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Удаление тэгов:\n1 - Включить \n0 - Выключить", reply_markup=menu_markup)

        return SWITHC_HANDLE_HASHTAG

    elif variant == "SWITHC_HANDLE_SMILES":

        keyboard = [[InlineKeyboardButton("Включить", callback_data='1')],
                    [InlineKeyboardButton("Выключить", callback_data='0')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Удаление смайлов:\n1 - Включить \n0 - Выключить", reply_markup=menu_markup)

        return SWITHC_HANDLE_SMILES

    return ConversationHandler.END


# Вызывается по команде
async def start(update, _):
    keyboard = [
        [InlineKeyboardButton("Добавить фильтр - удаление текста", callback_data='ADD_TEXT')],
        [InlineKeyboardButton("Добавить фильтр - стоп-пост", callback_data='ADD_STOP_POST')],
        [InlineKeyboardButton("Посмотреть фильтр - удаление текста", callback_data='CHECK_TEXT')],
        [InlineKeyboardButton("Посмотреть фильтр - стоп-пост", callback_data='CHECK_STOP_POST')],
        [InlineKeyboardButton("Удалить фильтр - удаление текста", callback_data='DELETE_TEXT')],
        [InlineKeyboardButton("Удалить фильтр - стоп-пост", callback_data='DELETE_STOP_POST')],
        [InlineKeyboardButton("Изменить удаление тэгов", callback_data='SWITHC_HANDLE_HASHTAG')],
        [InlineKeyboardButton("Изменить удаление смайлов", callback_data='SWITHC_HANDLE_SMILES')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

    return BUTTON


# Вызывается когда нажимается кнопка Назад
async def back(update, _):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Добавить фильтр - удаление текста", callback_data='ADD_TEXT')],
        [InlineKeyboardButton("Добавить фильтр - стоп-пост", callback_data='ADD_STOP_POST')],
        [InlineKeyboardButton("Посмотреть фильтр - удаление текста", callback_data='CHECK_TEXT')],
        [InlineKeyboardButton("Посмотреть фильтр - стоп-пост", callback_data='CHECK_STOP_POST')],
        [InlineKeyboardButton("Удалить фильтр - удаление текста", callback_data='DELETE_TEXT')],
        [InlineKeyboardButton("Удалить фильтр - стоп-пост", callback_data='DELETE_STOP_POST')],
        [InlineKeyboardButton("Изменить удаление тэгов", callback_data='SWITHC_HANDLE_HASHTAG')],
        [InlineKeyboardButton("Изменить удаление смайлов", callback_data='SWITHC_HANDLE_SMILES')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()

    await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)

    return BUTTON

async def main():
    app = Application.builder().token(token_bot).build()

    """В обработчике ConversationHandler() содержится логика разговора и представляет собой список, который хранит три состояния:
    1) Точку входа в разговор
    2) Этапы разговора
    3) Точку выхода из разговора
    """
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BUTTON: [CallbackQueryHandler(button)],
            BACK: [CallbackQueryHandler(back)],
            ADD_TEXT: [MessageHandler(filters.TEXT, hundler_add_filter_delete_text)],
            ADD_STOP_POST: [MessageHandler(filters.TEXT, hundler_add_filter_stop_post)],
            DELETE_TEXT: [MessageHandler(filters.TEXT, hundler_delete_filter_delete_text)],
            DELETE_STOP_POST: [MessageHandler(filters.TEXT, hundler_delete_filter_stop_post)],
            SWITHC_HANDLE_HASHTAG: [CallbackQueryHandler(handle_switch_handle_hashtag_bot)],
            SWITHC_HANDLE_SMILES: [CallbackQueryHandler(handle_switch_handle_smiles_bot)]
        },
        fallbacks=[]
    ))

    task1 = asyncio.create_task(start_bot())
    task2 = asyncio.create_task(input_cmd())

    tasks = [task1, task2]

    try:
        async with app:
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            await asyncio.gather(*tasks)
    except:
        KeyboardInterrupt()


if __name__ == "__main__":
    asyncio.run(main())
