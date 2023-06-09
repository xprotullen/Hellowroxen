# (c) @TheLx0980

import re, pyrogram
from pyrogram import filters, enums, Client
from config import Config
from bot import Bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

MEDIA_FILTER = enums.MessagesFilter.VIDEO 
BUTTONS = {}

@Client.on_message(filters.chat(Config.GROUPS) & filters.text)
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if len(message.text) > 2:
        group_id = str(message.chat.id)
        search_channel_id = get_search_channel_id(group_id)
        
        if search_channel_id:
            # Group ID exists in the database, perform search
            btn = []
            async for msg in client.USER.search_messages(Config.SEARCHCHANNEL_ID,query=message.text,filter=MEDIA_FILTER):
                file_name = msg.video.file_name
                msg_id = msg.id                     
                link = msg.link
                btn.append(
                    [InlineKeyboardButton(text=f"{file_name}",url=f"{link}")]
                )

            if not btn:
                return

            if len(btn) > 5: 
                btns = list(split_list(btn, 5)) 
                keyword = f"{message.chat.id}-{message.id}"
                BUTTONS[keyword] = {
                    "total" : len(btns),
                    "buttons" : btns
                }
            else:
                buttons = btn
                buttons.append(
                    [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
                )
                await message.reply_text(
                    f"<b> Here is the result for {message.text}</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

            data = BUTTONS[keyword]
            buttons = data['buttons'][0].copy()

            buttons.append(
                [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
            )    
            buttons.append(
                [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
            )

            await message.reply_text(
                    f"<b> Here is the result for {message.text}</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
