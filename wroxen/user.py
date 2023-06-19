# (c) @TheLx0980
# Year : 2023

from pyrogram import Client, __version__
from wroxen.vars import API_HASH, APP_ID, LOGGER, \
    USER_SESSION

class User(Client):
    def __init__(self):
        super().__init__(
            name="user_session",
            session_string=USER_SESSION,
            api_hash=Config.API_HASH,
            api_id=Config.APP_ID,
            workers=4
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username}  started!"
        )
        return self, usr_bot_me.id

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
