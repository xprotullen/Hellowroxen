# @thelx0980
from wroxen.text import ChatMSG
from wroxen.chek import get_channel_info
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums
from wroxen.wroxen import Wroxen
from wroxen.database.caption_db import set_caption, delete_caption, get_caption
import logging

media_filter = filters.document | filters.video | filters.audio
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("set_caption"))
async def set_caption_command(bot, message):
    user_id = message.from_user.id
    command_parts = message.text.split("::", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/set_caption {channel_id}::{channel_caption}`.")
        return

    channel_id = command_parts[0].split()[1]
    caption = command_parts[1]

    try:
        set_caption(user_id, channel_id, caption)
        await message.reply(f"Caption set for channel {channel_id}.")
    except ValueError:
        await message.reply("Channel already added in the database.")

    
@Client.on_message(filters.command("delete_info"))
async def delete_info_command(bot, message):
    user_id = message.from_user.id
    command_parts = message.text.split(" ", 2)

    if len(command_parts) < 2:
        await message.reply("Please provide the channel ID to delete.")
        return

    channel_id = command_parts[1]

    delete_info(user_id, channel_id)
    await message.reply(f"Channel ID and caption deleted for channel {channel_id}.")


@Client.on_message(filters.command("delete_caption"))
async def delete_caption_command(bot, message):
    user_id = message.from_user.id
    command_parts = message.text.split(" ", 2)

    if len(command_parts) < 2:
        await message.reply("Please provide the channel ID to delete the caption.")
        return

    channel_id = command_parts[1]

    deleted = delete_caption(user_id, channel_id)
    if deleted:
        await message.reply(f"Caption deleted for channel {channel_id}.")
    else:
        await message.reply("No caption found for the specified channel.")


@Client.on_message(filters.channel & (media_filter))
async def editing(bot, message):
    if message.from_user is None:
        return

    # Get the user ID
    user_id = message.from_user.id

    # Retrieve the channel ID and caption from the database
    channel_id, caption = get_channel_info(user_id)

    if channel_id and caption:
        try:
            media = message.document or message.video or message.audio
            caption_text = caption
           
        except:
            caption_text = ""
            pass

        if not channel_id.startswith("-100"):
            channel_id = "-100" + channel_id

        if (message.document or message.video or message.audio):
            if message.caption:
                file_caption = f"**{message.caption}**"
            else:
                fname = media.file_name
                filename = fname.replace("_", ".")
                file_caption = f"`{filename}`"

        try:
            await bot.edit_message_caption(
                chat_id=channel_id,
                message_id=message.message_id,
                caption=file_caption + "\n" + caption_text,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        except:
            pass
    else:        
        await bot.send_message(-1001970089414, ChatMSG.NOT_FOUND_TXT.format(message.chat.title, message.chat.id)




