import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application
from additional_files.notNeededWords import upd_delete_text, upd_stop_post

from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID

from actionWithDB import append_in_db_delete_text_from_cmd, append_in_db_stop_pots_from_cmd, \
    delete_from_db_delete_text_from_cmd, delete_from_db_text_stop_post_from_cmd, switch_handle_hashtag, \
    switch_handle_smiles

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
            await update.message.reply_text(f"Фильтр `{text[int(user_input) - 1]}` удалён", reply_markup=reply_markup)
            return BACK
        except IndexError:
            await update.message.reply_text("Фильтр отсутствует")

    else:
        if user_input in await upd_delete_text():

            await delete_from_db_delete_text_from_cmd(user_input)
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
            await update.message.reply_text(f"Фильтр `{text[int(user_input) - 1]}` стоп-пост удалён",
                                            reply_markup=reply_markup)
            return BACK

        except IndexError:
            await update.message.reply_text("Фильтр отсутствует")

    else:
        if user_input in await upd_stop_post():
            await delete_from_db_text_stop_post_from_cmd(user_input)
            await update.message.reply_text(f"Фильтр `{user_input}` стоп-пост удалён", reply_markup=reply_markup)
            return BACK
        else:
            await update.message.reply_text("Фильтр отсутствует")


async def handle_switch_handle_hashtag_bot(update, context):
    query = update.callback_query
    variant = query.data
    await query.answer()

    keyboard = [[InlineKeyboardButton("<< назад", callback_data='BACK')]]
    menu_markup = InlineKeyboardMarkup(keyboard)

    if variant == "1":
        await switch_handle_hashtag(int(variant))
        await query.edit_message_text(f"Удаление тэгов: Включено", reply_markup=menu_markup)
    elif variant == "0":
        await switch_handle_hashtag(int(variant))
        await query.edit_message_text(f"Удаление тэгов: Выключено", reply_markup=menu_markup)

    return BACK


async def handle_switch_handle_smiles_bot(update, context):
    query = update.callback_query
    variant = query.data
    await query.answer()

    keyboard = [[InlineKeyboardButton("<< назад", callback_data='BACK')]]
    menu_markup = InlineKeyboardMarkup(keyboard)

    if variant == "1":
        await switch_handle_smiles(int(variant))
        await query.edit_message_text(f"Удаление смайлов: Включено", reply_markup=menu_markup)
    elif variant == "0":
        await switch_handle_smiles(int(variant))
        await query.edit_message_text(f"Удаление смайлов: Выключено", reply_markup=menu_markup)

    return BACK
