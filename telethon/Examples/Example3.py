from telethon import TelegramClient, events
import logging
from tokens.tokens_telethon import API_ID, API_HASH

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
# Remember to use your own values from my.telegram.org!
api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

api_id = API_ID
api_hash = API_HASH
client = TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

# Отправляет сообщение hi, если был отправлен hello. Работа скрипта при этом продолжается
@client.on(events.NewMessage)
async def my_event_handler(event):
    print("wait event\n")
    if 'hello' in event.raw_text:
        await event.reply('hi!')

client.start()
client.run_until_disconnected()