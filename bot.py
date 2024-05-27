import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
import asyncio
import logging

from tokens.tokens import TOKEN_BOT, MY_ID
from additional_files.notNeededWords import upd_delete_text, upd_stop_post

from actionWithBot import handler_view_channel, handler_add_channel, handler_delete_channel, \
    hаndler_check_trigger_text, handler_add_filter_delete_text, handler_delete_trigger_delete_text, \
    handler_add_trigger_stop_post, handler_delete_trigger_stop_post, handle_switch_handle_hashtag_bot, \
    handle_switch_handle_smiles_bot, hаndler_check_trigger_stop_post

from ParsChannel import start_script
from actionWithCMD import input_cmd

token_bot = TOKEN_BOT
my_id = MY_ID

logging.basicConfig(filename='logs/app.log',
            format="\n[%(asctime)s]: %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            level=logging.INFO)

(BUTTON, BACK,
 ACTION_WITH_CHANNEL, ADD_CHANNEL, DELETE_CHANNEL,
 ACTION_WITH_FILTERS,
 ACTION_WITH_TRIGGER_TEXT, ADD_TRIGGER_TEXT, DELETE_TRIGGER_TEXT,
 ACTION_WITH_TRIGGER_STOP_POST, ADD_TRIGGER_STOP_POST, DELETE_TRIGGER_STOP_POST, CHECK_STOP_POST,
 ACTION_WITH_ANOTHER, SWITCH_HANDLE_HASHTAG, SWITCH_HANDLE_SMILES) = range(16)


# Действия с каналами
async def action_with_channel(update, _):

    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == "VIEW_CHANNEL":
        await handler_view_channel(update, _)
        return BACK

    elif variant == "ADD_CHANNEL":
        await query.edit_message_text("Напишите id и название канала через запятую")
        return ADD_CHANNEL

    elif variant == "DELETE_CHANNEL":
        await query.edit_message_text("Напишите название канала (не ID), которое нужно удалить")
        return DELETE_CHANNEL

    else:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
            [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
            [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)
        return BUTTON


# Действия с триггерами
async def action_with_filters(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == "ACTION_WITH_TEXT":
        keyboard = [
            [InlineKeyboardButton(">> Посмотреть триггеры для удаления из поста", callback_data='CHECK_TRIGGER_TEXT')],
            [InlineKeyboardButton(">> Добавить триггер для удаления из поста", callback_data='ADD_TRIGGER_TEXT')],
            [InlineKeyboardButton(">> Удалить триггер для удаления из поста", callback_data='DELETE_TRIGGER_TEXT')],
            [InlineKeyboardButton("<< В меню", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Выберете действие: ", reply_markup=menu_markup)
        return ACTION_WITH_TRIGGER_TEXT

    elif variant == "ACTION_WITH_STOP_POST":
        keyboard = [
            [InlineKeyboardButton(">> Посмотреть триггеры для стоп-пост", callback_data='CHECK_TRIGGER_STOP_POST')],
            [InlineKeyboardButton(">> Добавить триггер для стоп-пост", callback_data='ADD_TRIGGER_STOP_POST')],
            [InlineKeyboardButton(">> Удалить триггер для стоп-пост", callback_data='DELETE_TRIGGER_STOP_POST')],
            [InlineKeyboardButton("<< В меню", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Выберете действие: ", reply_markup=menu_markup)
        return ACTION_WITH_TRIGGER_STOP_POST

    else:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
            [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
            [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)
        return BUTTON


# Действия с триггерами для текста
async def action_with_trigger_text(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == 'CHECK_TRIGGER_TEXT':
        await hаndler_check_trigger_text(update, _)
        return BACK

    elif variant == 'ADD_TRIGGER_TEXT':
        await query.edit_message_text(
            "Внимание! Текст необходимо добавлять без точки в конце\nНапиши текст, который нужно добавить как фильтр для удаления из поста")
        return ADD_TRIGGER_TEXT

    elif variant == 'DELETE_TRIGGER_TEXT':
        reply_message = ""
        text = [text for text in await upd_delete_text()]

        for i in range(len(text)):
            reply_message += f"{i + 1}) {text[i]}\n"

        await query.edit_message_text(
            f"Напиши фильтр удаления из поста который нужно убрать из БД.\nМожно указать сам текст, либо выбери цифру:\n\n{reply_message}")
        return DELETE_TRIGGER_TEXT

    else:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
            [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
            [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)
        return BUTTON


async def action_with_trigger_stop_post(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == 'CHECK_TRIGGER_STOP_POST':
        await hаndler_check_trigger_stop_post(update, _)
        return BACK

    elif variant == 'ADD_TRIGGER_STOP_POST':
        await query.edit_message_text(
            "Внимание! Текст необходимо добавлять без точки в конце\nНапиши текст, который нужно добавить как фильтр для стоп-пост")
        return ADD_TRIGGER_STOP_POST

    elif variant == 'DELETE_TRIGGER_STOP_POST':
        reply_message = ""
        text = [text for text in await upd_stop_post()]

        for i in range(len(text)):
            reply_message += f"{i + 1}) {text[i]}\n"

        await query.edit_message_text(
            f"Напиши фильтр стоп-пост который нужно убрать из БД:\nМожно указать сам текст, либо выбери цифру:\n\n{reply_message}")
        return DELETE_TRIGGER_STOP_POST

    else:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
            [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
            [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)
        return BUTTON


async def action_with_another(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == "SWITCH_HANDLE_HASHTAG":
        keyboard = [[InlineKeyboardButton("Включить", callback_data='1')],
                    [InlineKeyboardButton("Выключить", callback_data='0')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Удаление тэгов:\n1 - Включить \n0 - Выключить", reply_markup=menu_markup)

        return SWITCH_HANDLE_HASHTAG

    elif variant == "SWITCH_HANDLE_SMILES":
        keyboard = [[InlineKeyboardButton("Включить", callback_data='1')],
                    [InlineKeyboardButton("Выключить", callback_data='0')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Удаление смайлов:\n1 - Включить \n0 - Выключить", reply_markup=menu_markup)

        return SWITCH_HANDLE_HASHTAG

    else:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
            [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
            [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)
        return BUTTON


async def button(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()

    if variant == "ACTION_WITH_CHANNEL":
        keyboard = [[InlineKeyboardButton("> Посмотреть текущие каналы", callback_data='VIEW_CHANNEL')],
                    [InlineKeyboardButton("> Добавить канал", callback_data='ADD_CHANNEL')],
                    [InlineKeyboardButton("> Удалить канал", callback_data='DELETE_CHANNEL')],
                    [InlineKeyboardButton("< В меню", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Выберете действие: ", reply_markup=menu_markup)
        return ACTION_WITH_CHANNEL

    elif variant == "ACTION_WITH_FILTERS":
        keyboard = [[InlineKeyboardButton("> Действие с триггерами по удалению текста из поста",
                                          callback_data='ACTION_WITH_TEXT')],
                    [InlineKeyboardButton("> Действие с триггерами для стоп-пост",
                                          callback_data='ACTION_WITH_STOP_POST')],
                    [InlineKeyboardButton("< В меню", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Выберете действие: ", reply_markup=menu_markup)
        return ACTION_WITH_FILTERS

    elif variant == "ACTION_WITH_ANOTHER":
        keyboard = [[InlineKeyboardButton("> Переключить удаление хэштегов", callback_data='SWITCH_HANDLE_HASHTAG')],
                    [InlineKeyboardButton("> Переключить удаление смайлов", callback_data='SWITCH_HANDLE_SMILES')],
                    [InlineKeyboardButton("< В меню", callback_data='BACK')]]
        menu_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Выберете действие: ", reply_markup=menu_markup)
        return ACTION_WITH_ANOTHER

    return ConversationHandler.END


# Вызывается по команде
async def start(update, _):
    if update.message.chat.id != my_id:
        print(update.message.chat.id)
        await _.bot.send_message(chat_id=update.effective_chat.id, text="Access Denied")

    else:
        keyboard = [
            [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
            [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
            [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

        return BUTTON


# Вызывается когда нажимается кнопка Назад
async def back(update, _):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Действие с каналами", callback_data='ACTION_WITH_CHANNEL')],
        [InlineKeyboardButton("Действие с фильтрами", callback_data='ACTION_WITH_FILTERS')],
        [InlineKeyboardButton("Действие с тэгами/смайлами", callback_data='ACTION_WITH_ANOTHER')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()

    await query.edit_message_text('Пожалуйста, выберите:', reply_markup=reply_markup)

    return BUTTON


async def main():
    app = Application.builder().token(token_bot).build()

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BUTTON: [CallbackQueryHandler(button)],
            BACK: [CallbackQueryHandler(back)],

            ACTION_WITH_CHANNEL: [CallbackQueryHandler(action_with_channel)],
            ADD_CHANNEL: [MessageHandler(filters.TEXT, handler_add_channel)],
            DELETE_CHANNEL: [MessageHandler(filters.TEXT, handler_delete_channel)],

            ACTION_WITH_FILTERS: [CallbackQueryHandler(action_with_filters)],

            ACTION_WITH_TRIGGER_TEXT: [CallbackQueryHandler(action_with_trigger_text)],
            ADD_TRIGGER_TEXT: [MessageHandler(filters.TEXT, handler_add_filter_delete_text)],
            DELETE_TRIGGER_TEXT: [MessageHandler(filters.TEXT, handler_delete_trigger_delete_text)],

            ACTION_WITH_TRIGGER_STOP_POST: [CallbackQueryHandler(action_with_trigger_stop_post)],
            ADD_TRIGGER_STOP_POST: [MessageHandler(filters.TEXT, handler_add_trigger_stop_post)],
            DELETE_TRIGGER_STOP_POST: [MessageHandler(filters.TEXT, handler_delete_trigger_stop_post)],

            ACTION_WITH_ANOTHER: [CallbackQueryHandler(action_with_another)],
            SWITCH_HANDLE_HASHTAG: [CallbackQueryHandler(handle_switch_handle_hashtag_bot)],
            SWITCH_HANDLE_SMILES: [CallbackQueryHandler(handle_switch_handle_smiles_bot)]
        },
        fallbacks=[]
    ))

    task1 = asyncio.create_task(start_script())
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
