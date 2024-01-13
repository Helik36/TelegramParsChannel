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

# Сохраняет картинку
# await client.download_media(message_id[0].photo, "C:/Users/Helik/Desktop/telegram/pythonProject/telethon/media")

# Проходиться по сообщениям до указанного лимита, далее можно из них можно вытянут инфу
# async for get_mess_id in client.iter_messages(-1002076831448, limit=1):
#     print(get_mess_id)

# Пересылает сообщения из канала test в канал PL c поветкой forward
# mass_get_id = []
# async for get_mess_id in client.iter_messages(-1002076831448, limit=2):
#     mass_get_id.append(get_mess_id.id)
#     print(get_mess_id.text)
#     print(get_mess_id.id)
# await client.forward_messages(-1001999849557, mass_get_id, -1002076831448)
# mass_get_id.clear()
