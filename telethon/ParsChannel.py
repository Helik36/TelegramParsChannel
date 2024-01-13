from telethon import TelegramClient
import logging
from tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash)

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL


async def main():
    # mass_get_id = []

    # Получаю информацию о своих сообщения, с установленым лимитом до 3х сообщений
    # async for get_mess_id in client.iter_messages(channel_test, limit=3):
    #     print(get_mess_id.text)
    #     mass_get_id.append(get_mess_id.id)

    # print(mass_get_id)
    # mass_get_id.clear()

    # # Пересылает сообщения от меня в канал
    # await client.forward_messages(-1002076831448, mass_get_id, 'me')

    # Пересылает сообщения из канала ко мне
    # async for get_mess_id in client.iter_messages(-1002076831448, limit=2):
    #     mass_get_id.append(get_mess_id.id)
    #     print(get_mess_id.text)
    #     print(get_mess_id.id)
    # await client.forward_messages('me', mass_get_id, -1002076831448)

    # mass_get_id.clear()

    # Пересылает сообщения из канала test в канал PlayMood
    # async for get_mess_id in client.iter_messages(-1002076831448, limit=2):
    #     mass_get_id.append(get_mess_id.id)
    #     print(get_mess_id.text)
    #     print(get_mess_id.id)
    # await client.forward_messages(-1001999849557, mass_get_id, -1002076831448)

    # mass_get_id.clear()

    # check = None

    # async for get_mess_id in client.iter_messages(-1002076831448, limit=1):
    #     check = get_mess_id.text
    #
    # message = await client.get_messages(-1002076831448)
    # print(message.message)

    # photos = await client.get_messages(-1002076831448, 0, filter=InputMessagesFilterPhotos)
    # print(photos.total)

    # Получаем информацию о последнем сообщении (показывает только одно)
    # message_id = await client.get_messages(channel_test)
    # data_message = message_id[0]
    # data_message_id = data_message.id
    # data_message_text = data_message.message
    # data_message_media_photo = data_message.photo

    # print(data_message) # Печатает всю инфу о сообщении
    # print(data_message_id)  # Печатает id сообщения
    # print(data_message_text) #  печатает текст сообщения
    # print(data_message_media_photo) # Печатает информацию о картинке


    # Получаем последние сообщения
    # Лимит показывает отправленные объекты. Т.е в телеге может быть 1 сообщение, у него есть 2 фото и текст. Это 3 разных объекта
    # Далее работается также как и с get_message
    pasring_photos = []
    pasring_text = []
    async for data_message in client.iter_messages(channel_test, limit=2):
        print(data_message)
        print(data_message.photo)

        if data_message.photo is not None:
            pasring_photos.append(data_message.photo)
        else:
            pass

        if data_message.message != '':
            pasring_text.append(data_message.message)
        else:
            pass

    await client.send_file(channel_PL, pasring_photos, caption=pasring_text[0])

    print(pasring_text)
    print(pasring_photos[0])
    print(pasring_photos[1])


    # Сохраняет картинку
    # await client.download_media(message_id[0].photo, "C:/Users/Helik/Desktop/telegram/pythonProject/telethon/media")

    # await client.send_file(-1001999849557, data_message_media_photo, caption = data_message_text)

    # message_1337 = await client.get_messages(-1002076831448, ids=)
    # print(message_1337)
    # await client.send_message(-1001999849557, check)

    # mass_get_id.clear()


with client:
    client.loop.run_until_complete(main())

    """
    Парсим сообщение. качает фотки в папку, прикрепляем к сообщению, отправляем, удаляем фотки из папки
    """
