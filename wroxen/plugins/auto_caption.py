# @thelx0980

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
    command_parts = message.text.split(" ", 3)

    if len(command_parts) < 4:
        await message.reply("Please provide both the channel ID and the caption.")
        return

    channel_id = command_parts[1]
    caption = command_parts[2]

    set_caption(user_id, channel_id, caption)
    await message.reply(f"Caption set for channel {channel_id}.")

    
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

def delete_caption(user_id, channel_id):
    result = captions_collection.delete_one({"user_id": user_id, "channel_id": channel_id})
    return result.deleted_count > 0
  
@Client.on_message(filters.channel & (media_filter))
async def editing(bot, message):
    channel_id = message.chat.id
    user_caption = get_caption(message.from_user.id, channel_id)

    if user_caption:
        try:
            media = message.document or message.video or message.audio
            caption_text = user_caption
        except:
            caption_text = ""
            pass

        if (message.document or message.video or message.audio):
            if message.caption:
                file_caption = f"**{message.caption}**"
            else:
                fname = media.file_name
                filename = fname.replace("_", ".")
                file_caption = f"`{filename}`"

        try:
            if caption_position == "top":
                await bot.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    caption=file_caption + "\n" + caption_text,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
        except:
            pass
