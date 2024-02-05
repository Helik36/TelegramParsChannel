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
ASD = range(1)

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


async def  hundler_add_filter_delete_text(update, context):
    user_input = update.message.text
    print(user_input)


async def add_filter_delete_text(update, context):
    await update.message.reply_text("Напиши текст, который нужно добвить как фильтр для удаления из поста")
    # переходим к этапу
    return ASD



async def add_filter_stop_post(update, context):
    pass


async def get_filter_delete_text(update, context):
    # await update.message.reply_text("qwe")
    await update.message.reply_text(get_from_db_delete_text())


async def get_filter_stop_post(update, context):
    await update.message.reply_text(get_from_db_stop_post_text())


async def delete_filter_delete_text(update, context):
    pass


async def delete_filter_stop_post(update, context):
    pass

def main():
    # app = Application.builder().token(token_bot).build()

    """В обработчике ConversationHandler() содержится логика разговора и представляет собой список, который хранит три состояния:
    1) Точку входа в разговор
    2) Этапы разговора
    3) Точку выхода из разговора
    """
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("add_filter_delete_text", add_filter_delete_text)],
        states={
            ASD: [MessageHandler(filters.TEXT, hundler_add_filter_delete_text)]
        },
        fallbacks=[]
    ))

    app.add_handler(CommandHandler("add_filter_stop_post", add_filter_stop_post))
    app.add_handler(CommandHandler("get_filter_delete_text", get_filter_delete_text))
    app.add_handler(CommandHandler("get_filter_stop_post", get_filter_stop_post))
    app.add_handler(CommandHandler("delete_filter_delete_text", delete_filter_delete_text))
    app.add_handler(CommandHandler("delete_filter_stop_post", delete_filter_stop_post))


    # Пересылает сообщения
    # app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), parsing_channel))

    app.run_polling()


"""
add_filter_delete_text - Добавить фильтр для удаления текста из поста
add_filter_stop_post - Добавить фильтр для стоп-пост
get_filter_delete_text - Посмотреть текущие фильтры на удаление текста из поста
get_filter_stop_post - Посмотреть текущие фильтры на стоп-пост
del_filter_delete_text - Удалить фильтр на удаление текста из поста
del_filter_stop_post - Удалить фильтр из стоп-пост
"""

if __name__ == "__main__":
    main()
