import asyncio
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID

from actionWithBot import hundler_add_filter_delete_text, hundler_add_filter_stop_post, \
    hundler_delete_filter_delete_text, hundler_delete_filter_stop_post, add_filter_delete_text, add_filter_stop_post, \
    get_filter_delete_text, get_filter_stop_post, delete_filter_delete_text, delete_filter_stop_post

from ParsChannel import start_bot
from async_cmd import input_cmd

token_bot = TOKEN
my_id = MY_ID
my_channel_id = MY_CHANNEL_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

id_channel_pasring = ID_CHANNEL_ID
# app = Application.builder().token(token_bot).build()

BUTTON, BACK, ADD_TEXT, ADD_STOP_POST, DELETE_TEXT, DELETE_STOP_POST, CHECK_TEXT, CHECK_STOP_POST = range(8)


"""
Две нижние функции нужны, чтобы вместо меню, которое делает FatherBot, можно было сделать самому
красивое и изменяемой сообщение, которое выводит бот
"""


async def button(update, _):
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    await query.answer()
    print(variant)

    if variant == "ADD_TEXT":
        await add_filter_delete_text(update, _)
        return ADD_TEXT

    elif variant == "ADD_STOP_POST":
        await query.edit_message_text("Напиши текст, который нужно добвить как фильтр для стоп-пост")
        return ADD_STOP_POST

    elif variant == "CHECK_TEXT":
        await get_filter_delete_text(update, _)
        return BACK

    elif variant == "CHECK_STOP_POST":
        await get_filter_stop_post(update, _)
        return BACK

    elif variant == "DELETE_TEXT":
        await delete_filter_delete_text(update, _)
        return DELETE_TEXT

    elif variant == "DELETE_STOP_POST":
        await delete_filter_stop_post(update, _)
        return DELETE_STOP_POST

    return ConversationHandler.END


# Вызывается по команде
async def start(update, _):
    keyboard = [
        [InlineKeyboardButton("Добавить фильтр - удаление текста", callback_data='ADD_TEXT')],
        [InlineKeyboardButton("Добавить фильтр - стоп-пост", callback_data='ADD_STOP_POST')],
        [InlineKeyboardButton("Посмотреть фильтр - удаление текста", callback_data='CHECK_TEXT')],
        [InlineKeyboardButton("Посмотреть фильтр - стоп-пост", callback_data='CHECK_STOP_POST')],
        [InlineKeyboardButton("Удалить фильтр - удаление текста", callback_data='DELETE_TEXT')],
        [InlineKeyboardButton("Удалить фильтр - стоп-пост", callback_data='DELETE_STOP_POST')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # для версии 20.x необходимо использовать оператор await
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
        [InlineKeyboardButton("Удалить фильтр - стоп-пост", callback_data='DELETE_STOP_POST')]
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
        entry_points=[CommandHandler("start", start),
                      CommandHandler("add_filter_delete_text", add_filter_delete_text),
                      CommandHandler("add_filter_stop_post", add_filter_stop_post),
                      CommandHandler("get_filter_delete_text", get_filter_delete_text),
                      CommandHandler("get_filter_stop_post", get_filter_stop_post),
                      CommandHandler("del_filter_delete_text", delete_filter_delete_text),
                      CommandHandler("del_filter_stop_post", delete_filter_stop_post)],
        states={
            BUTTON: [CallbackQueryHandler(button)],
            BACK: [CallbackQueryHandler(back)],
            ADD_TEXT: [MessageHandler(filters.TEXT, hundler_add_filter_delete_text)],
            ADD_STOP_POST: [MessageHandler(filters.TEXT, hundler_add_filter_stop_post)],
            DELETE_TEXT: [MessageHandler(filters.TEXT, hundler_delete_filter_delete_text)],
            DELETE_STOP_POST: [MessageHandler(filters.TEXT, hundler_delete_filter_stop_post)]
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
