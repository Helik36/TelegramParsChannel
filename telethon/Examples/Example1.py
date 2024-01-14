from telethon import TelegramClient

from tokens.tokens_telethon import API_ID, API_HASH

# Use your own values from my.telegram.org
api_id = API_ID
api_hash = API_HASH

# system_version='4.16.30-vxCUSTOM' нужна, чтобы не выбивала сессии из других устройств 
# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('anon', api_id, api_hash, system_version='4.16.30-vxCUSTOM') as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))

"""
In the first line, we import the class name so we can create an instance of the client. 
Then, we define variables to store our API ID and hash conveniently.

At last, we create a new TelegramClient instance and call it client. 
We can now use the client variable for anything that we want, such as sending a message to ourselves.
"""