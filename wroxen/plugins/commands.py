# (c) TheLx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from wroxen import Wroxen
from wroxen.text import ChatMSG

@Wroxen.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    await message.reply(
        text=ChatMSG.START_TXT.format(message.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup = url_button,
        quote=True
    )
    

@Wroxen.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(client, message):
    await message.reply(
        text=ChatMSG.ABOUT_TXT,
        disable_web_page_preview=True,
        reply_markup = url_button,
        quote=True
    )

    
