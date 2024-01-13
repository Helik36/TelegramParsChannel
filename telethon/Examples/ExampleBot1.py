from telethon.sync import TelegramClient
from ..tokens_telethon import API_ID, API_HASH, TOKEN_BOT

api_id = API_ID
api_hash = API_HASH
bot_token = TOKEN_BOT

# We have to manually call "start" if we want an explicit bot token
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# But then we can use the client instance as usual
with bot:
    pass

# q