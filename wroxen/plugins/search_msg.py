# (c) @TheLx0980

HELLO = """
import re, pyrogram
from pyrogram import filters, enums, Client
from config import Config
from bot import Bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from wroxen.database.search_msg import add_group_search, get_search_channel_id, update_group_search, \
   delete_group_search

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

MEDIA_FILTER = enums.MessagesFilter.VIDEO 
BUTTONS = {}

@Client.on_message(filters.command("set_search_id") & filters.user(944747838))
async def set_search_id_command(bot, message):
    command_parts = message.text.split(" ", 2)

    if len(command_parts) != 3:
        await message.reply("Invalid format. Please use the format `/set_search_id {group_id} {search_channel_id}`.")
        return

    group_id = command_parts[1]
    search_channel_id = command_parts[2]

    if not group_id.startswith("-100"):
        group_id = "-100" + group_id

    if not search_channel_id.startswith("-100"):
        search_channel_id = "-100" + search_channel_id

    existing_search_channel_id = get_search_channel_id(group_id)

    if existing_search_channel_id:
        await message.reply("Your group ID already exists in the database.")
        return

    try:
        add_group_search(group_id, search_channel_id)
        await message.reply(f"Search ID set for group {group_id}.")
    except:
        await message.reply("Failed to set Search ID for group.")

@Client.on_message(filters.command("update_search_id") & filters.user(944747838))
async def update_search_id_command(bot, message):
    command_parts = message.text.split(" ", 2)

    if len(command_parts) != 3:
        await message.reply("Invalid format. Please use the format `/update_search_id {group_id} {search_channel_id}`.")
        return

    group_id = command_parts[1]
    search_channel_id = command_parts[2]

    if not group_id.startswith("-100"):
        group_id = "-100" + group_id

    if not search_channel_id.startswith("-100"):
        search_channel_id = "-100" + search_channel_id

    existing_search_channel_id = get_search_channel_id(group_id)

    if not existing_search_channel_id:
        await message.reply("Group ID does not exist in the database.")
        return

    try:
        update_group_search(group_id, search_channel_id)
        await message.reply(f"Search ID updated for group {group_id}.")
    except:
        await message.reply("Failed to update Search ID for group.")


@Client.on_message(filters.command("delete_search_id") & filters.user(944747838))
async def delete_search_id_command(bot, message):
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/delete_search_id {group_id}`.")
        return

    group_id = command_parts[1]

    if not group_id.startswith("-100"):
        group_id = "-100" + group_id

    existing_search_channel_id = get_search_channel_id(group_id)

    if not existing_search_channel_id:
        await message.reply("Group ID does not exist in the database.")
        return

    try:
        delete_group_search(group_id)
        await message.reply(f"Search ID deleted for group {group_id}.")
    except:
        await message.reply("Failed to delete Search ID for group.")



@Client.on_message(filters.chat(Config.GROUPS) & filters.text)
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if len(message.text) > 2:
        group_id = str(message.chat.id)
        search_channel_id = get_search_channel_id(group_id)
        search_id = int(search_channel_id)
        
        if search_channel_id:
            # Group ID exists in the database, perform search
            btn = []
            async for msg in client.USER.search_messages(search_id,query=message.text,filter=MEDIA_FILTER):
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
"""
