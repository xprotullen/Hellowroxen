# (©) TheLx0980

import os


#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))

class Wroxen(Client):
    def __init__(self):
        super().__init__(
            name='wroxen_Bot',
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"@{me.username} Is Started!")
        try:
            await self.send_message(LOG_CHANNEL, "Bot Restarted!")
        except:
            pass

    async def stop(self, *args):
        await super().stop()              
        logging.info("Bot stopped. Bye.")
        
Wroxen().run()
