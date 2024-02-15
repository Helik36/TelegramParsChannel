import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ConversationHandler
from additional_files.notNeededWords import upd_delete_text, upd_stop_post

from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID

from actionWithDB import append_in_db_delete_text_from_cmd, append_in_db_stop_pots_from_cmd, \
    delete_from_db_delete_text_from_cmd, delete_from_db_text_stop_post_from_cmd

token_bot = TOKEN
my_id = MY_ID
my_channel_id = MY_CHANNEL_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

id_channel_pasring = ID_CHANNEL_ID
app = Application.builder().token(token_bot).build()

BUTTON, BACK, ADD_TEXT, ADD_STOP_POST, DELETE_TEXT, DELETE_STOP_POST, CHECK_TEXT, CHECK_STOP_POST = range(8)


# Получаю информацию о пооследнем собщении от себя и копирую в канал
# Копирование происходит с вложениями и эффектами на них
async def parsing_channel(update: Update, context):
    print(update.message)
    print(update.message.chat_id)

    # Проверяю, что Id совпадает с моим. Если нет, отказ в доступе
    if update.message.chat.id != my_id:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access Denied")
    else:
        await context.bot.copyMessage(my_channel_id, my_id, update.message.message_id)


async def hundler_add_filter_delete_text(update, context):
    keyboard = [[InlineKeyboardButton("<< В меню", callback_data='BACK')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_input = update.message.text
    await append_in_db_delete_text_from_cmd(user_input)
    await update.message.reply_text(f"Фильтр `{user_input}` добавлен", reply_markup=reply_markup)
    return BACK


async def hundler_add_filter_stop_post(update, context):
    keyboard = [[InlineKeyboardButton("<< Меню", callback_data='BACK')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_input = update.message.text
    await append_in_db_stop_pots_from_cmd(user_input)
    await update.message.reply_text(f"Фильтр `{user_input}` добавлен", reply_markup=reply_markup)
    return BACK


async def hundler_delete_filter_delete_text(update, context):
    keyboard = [[InlineKeyboardButton("<< в меню", callback_data='BACK')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_input = update.message.text
    text = [text for text in await upd_delete_text()]

    if user_input.isdigit():
        try:
            await delete_from_db_delete_text_from_cmd(text[int(user_input) - 1])
            await get_filter_delete_text(update, context)
            await update.message.reply_text(f"Фильтр `{text[int(user_input) - 1]}` удалён", reply_markup=reply_markup)
            return BACK
        except IndexError:
            await update.message.reply_text("Фильтр отсутствует")

    else:
        if user_input in await upd_delete_text():

            await delete_from_db_delete_text_from_cmd(user_input)
            await get_filter_delete_text(update, context)
            await update.message.reply_text(f"Фильтр `{user_input}` удалён", reply_markup=reply_markup)
            return BACK
        else:
            await update.message.reply_text("Фильтр отсутствует")

async def hundler_delete_filter_stop_post(update, context):
    keyboard = [[InlineKeyboardButton("<< в меню", callback_data='BACK')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_input = update.message.text
    text = [text for text in await upd_stop_post()]

    if user_input.isdigit():
        try:
            await delete_from_db_text_stop_post_from_cmd(text[int(user_input) - 1])
            await get_filter_stop_post(update, context)
            await update.message.reply_text(f"Фильтр `{text[int(user_input) - 1]}` стоп-пост удалён",
                                            reply_markup=reply_markup)
            return BACK

        except IndexError:
            await update.message.reply_text("Фильтр отсутствует")

    else:
        if user_input in await upd_stop_post():
            await delete_from_db_text_stop_post_from_cmd(user_input)
            await get_filter_stop_post(update, context)
            await update.message.reply_text(f"Фильтр `{user_input}` стоп-пост удалён", reply_markup=reply_markup)
            return BACK
        else:
            await update.message.reply_text("Фильтр отсутствует")

async def add_filter_delete_text(update, context):
    if hasattr(update.message, "text"):
        await update.message.reply_text("Напиши текст, который нужно добвить как фильтр для удаления из поста")
        return ADD_TEXT

    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Напиши текст, который нужно добвить как фильтр для удаления из поста")


async def add_filter_stop_post(update, context):
    if hasattr(update.message, "text"):
        await update.message.reply_text("Напиши текст, который нужно добвить как фильтр для стоп-пост")
        return ADD_STOP_POST
    
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Напиши текст, который нужно добвить как фильтр для стоп-пост")


async def get_filter_delete_text(update, context):
    reply_message = ""
    text = [text for text in await upd_delete_text()]

    for i in range(len(text)):
        reply_message += f"{i + 1}) {text[i]}\n"

    # Трай нужен т.к. ручка была вызваза из InlineKeyboardButton, то отправка сообщения может вызвать ошибку.
    try:
        await update.message.reply_text(reply_message)
        return ConversationHandler.END

    except:
        query = update.callback_query
        await query.answer()
        keyboard = [[InlineKeyboardButton("<< назад", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Фильтра для удаления текста:\n\n{reply_message}", reply_markup=menu_markup)


async def get_filter_stop_post(update, context):
    reply_message = ""
    text = [text for text in await upd_stop_post()]

    for i in range(len(text)):
        reply_message += f"{i + 1}) {text[i]}\n"

    # Трай нужен т.к. ручка была вызваза из InlineKeyboardButton, то отправка сообщения может вызвать ошибку.
    try:
        await update.message.reply_text(reply_message)
        return ConversationHandler.END
    except:
        query = update.callback_query
        await query.answer()
        keyboard = [[InlineKeyboardButton("<< назад", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Фильтр стоп-пост:\n\n{reply_message}", reply_markup=menu_markup)


async def delete_filter_delete_text(update, context):
    reply_message = ""
    text = [text for text in await upd_delete_text()]

    for i in range(len(text)):
        reply_message += f"{i + 1}) {text[i]}\n"

    try:
        await update.message.reply_text(
            f"Напиши фильтр удаления из поста который нужно убрать из БД:\n\n{reply_message}")
        return DELETE_TEXT
    except:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(f"Напиши фильтр удаления из поста который нужно убрать из БД:\n\n{reply_message}")


async def delete_filter_stop_post(update, context):
    reply_message = ""
    text = [text for text in await upd_stop_post()]

    for i in range(len(text)):
        reply_message += f"{i + 1}) {text[i]}\n"

    try:
        await update.message.reply_text(f"Напиши фильтр стоп-пост который нужно убрать из БД:\n\n{reply_message}")
        return DELETE_STOP_POST
    except:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(f"Напиши фильтр стоп-пост который нужно убрать из БД:\n\n{reply_message}")


"""
add_filter_delete_text - Добавить фильтр для удаления текста из поста
add_filter_stop_post - Добавить фильтр для стоп-пост
get_filter_delete_text - Посмотреть текущие фильтры на удаление текста из поста
get_filter_stop_post - Посмотреть текущие фильтры на стоп-пост
del_filter_delete_text - Удалить фильтр на удаление текста из поста
del_filter_stop_post - Удалить фильтр из стоп-пост
"""