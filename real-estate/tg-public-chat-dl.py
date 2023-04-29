# https://my.telegram.org/apps
# https://docs.telethon.dev/en/stable/basic/quick-start.html

import os
from telethon import TelegramClient
import time
import json


api_id = 00000000
api_hash = '<TOKEN>'
client = TelegramClient('anon', api_id, api_hash)

async def main():
    me = await client.get_me()
    print(me.stringify())
    username = me.username
    print(username)
    print(me.phone)

    chatname = 'ru_avsallar'

    dt = time.strftime("%Y%m%d-%H%M%S")
    filename = chatname + '-' + dt +'.json'
    dictMsg = {}

    async for message in client.iter_messages(chatname):

        print('Processing message', str(message.id))
        msg = str(message.raw_text)

        if ('Авсаллар' in msg and
            'прода' in msg and
            'квартира' in msg and
            '€' in msg):

            dictMsg[message.id] = [str(message.date), str(message.raw_text)]

            msgFile = open(filename, "w")
            json.dump(dictMsg, msgFile, indent=4, sort_keys=True, ensure_ascii=False)
            msgFile.close()

            print(msg)

with client:
    client.loop.run_until_complete(main())
