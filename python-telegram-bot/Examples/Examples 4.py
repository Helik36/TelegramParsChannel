import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from tokens.tokens_tele_bot import TOKEN, MY_ID, MY_CHANNEL_ID, ID_CHANNEL_ID
from actionWithDB import append_in_db_delete_text_from_cmd, append_in_db_stop_pots_from_cmd, \
    delete_from_db_delete_text_from_cmd, delete_from_db_text_stop_post_from_cmd, get_from_db_delete_text, \
    get_from_db_stop_post_text

token_bot = TOKEN
my_id = MY_ID
my_channel_id = MY_CHANNEL_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

id_channel_pasring = ID_CHANNEL_ID
app = Application.builder().token(token_bot).build()

"""
Задача на следующую работу написаны не по порядку (Если не появяться какие-либо вытекающие):

1) Всё таки понять, как разделить разный процесс на отдельные функции

2) Вытаскивать текст, сохранять, возможно как-то видоизменить (убрать лишние слова) далее сохранённый текст отправлять 
2.1) В таком случае - подумать, что делать с вложениями

3) Подумать над каналами для парсинга

3) Узнать на счёт ChatGPT, подключить, настроить (для задачи 2, чтобы был уникальный контент. Узнать ПРОМТ.

4) Сделать Парсер сайтов и Реддита!

5) Залить на хост [upd: нужен VPS]

6) Доделать логирование

7) Добавить массив, куда можно добавлять id канал, от куда потом в другой функции они будут считываться и парситься
"""


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


# Функция парсинга каналов
async def getMessId(update: Update, context):
    print(update.message)
    print(update.message.chat_id)


async def start_callback(update, context):
    print(update.message)
    print(update.message.chat_id)
    await update.message.reply_text("Hello! I'm your bot.")


# Меню в виде одного сообщения одной строкой постоянно меняющейся
async def start_callback(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)


async def button(update, _):
    query = update.callback_query
    variant = query.data

    await query.answer()
    await query.edit_message_text(text=f"Выбранный вариант: {variant}")


def main():
    # app = Application.builder().token(token_bot).build()

    # Создание обработчиков
    # CommandHandler - Для создания /команд
    # MessageHandler - Настраивается отдельно
    app.add_handler(CommandHandler('start', start_callback))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), getMessId))

    # Пересылает сообщения
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), parsing_channel))

    app.run_polling()


if __name__ == "__main__":
    main()
