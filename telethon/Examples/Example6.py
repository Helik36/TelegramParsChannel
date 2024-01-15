from tokens.tokens_telethon import API_ID, API_HASH, CHANNEL_TEST, CHANNEL_PL
from telethon import TelegramClient, events

import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)


api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

channel_test = CHANNEL_TEST
channel_PL = CHANNEL_PL

@client.on(events.NewMessage(chats='me'))
async def handler(event):
    if event.grouped_id:
        return    # ignore messages that are gallery here

    await client.send_message(channel_test, event.message)

# Копирует и пересылает фото не разделяя их на разные сообщения
@client.on(events.Album(chats='me'))
async def handler(event):
    await client.send_file(channel_test, event.messages, caption=event.original_update.message.message)

client.start()
client.run_until_disconnected()