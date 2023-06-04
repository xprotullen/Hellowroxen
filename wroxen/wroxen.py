# (©) TheLx0980

import logging
import logging.config
import os
from . import APP_ID, API_HASH, TG_BOT_TOKEN
#-------------------------------------------------------------------------------------------------#
from pyrogram import Client, __version__ 

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Wroxen(Client):
    def __init__(self):
        super().__init__(
            name='wroxen_Bot',
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=50,
            plugins={"root": "wroxen/plugins"},
            sleep_threshold=5
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"@{me.username} Is Started!")
        try:
            await self.send_message(OWNER_ID, "Bot Restarted!")
        except:
            pass

    async def stop(self, *args):
        await super().stop()              
        logging.info("Bot stopped. Bye.")
        

