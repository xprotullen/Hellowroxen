# (c) @thelx0980

from wroxen.text import ChatMSG
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums
from wroxen.wroxen import Wroxen
from wroxen.database.caption_db import set_caption, delete_caption, get_caption, captions_collection, channels_collection, \
    is_channel_added

import logging

media_filter = filters.document | filters.video | filters.audio
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("update_caption"))
async def update_caption_command(bot, message):
    command_parts = message.text.split("::", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/update_caption {channel_id}::{new_caption}`.")
        return

    channel_id = command_parts[0].split()[1]
    new_caption = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    if not is_channel_added(channel_id):
        await message.reply("The channel is not added in the database.")
        return

    try:
        update_caption(channel_id, new_caption)
        await message.reply(f"Caption updated for channel {channel_id}.\n\n{new_caption}")
    except ValueError:
        await message.reply("An error occurred while updating the caption in the database.")


@Client.on_message(filters.command("caption"))
async def get_caption_command(bot, message):
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/caption {channel_id}`.")
        return

    channel_id = command_parts[1]
    caption = get_caption(channel_id)

    if caption:
        await message.reply(f"The caption for channel {channel_id} is:\n{caption}")
    else:
        await message.reply(f"No caption found for channel {channel_id}.")


@Client.on_message(filters.command("set_caption"))
async def set_caption_command(bot, message):
    command_parts = message.text.split("::", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/set_caption {channel_id}::{channel_caption}`.")
        return

    channel_id = command_parts[0].split()[1]
    caption = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    try:
        add_channel(channel_id, caption)
        await message.reply(f"Caption set for channel {channel_id}.\n\n{caption}")
    except ValueError:
        await message.reply("Channel already added in the database.")


@Client.on_message(filters.command("cleardb"))
async def delete_all_info_command(bot, message):
    channels_collection.delete_many({})
    await message.reply("All database info deleted.")


@Client.on_message(filters.command("delete_caption"))
async def delete_caption_command(bot, message):
    command_parts = message.text.split(" ", 2)

    if len(command_parts) < 2:
        await message.reply("Please provide the channel ID to delete the caption.")
        return

    channel_id = command_parts[1]

    deleted = delete_channel(channel_id)
    if deleted:
        await message.reply(f"Caption deleted for channel {channel_id}.")
    else:
        await message.reply("No caption found for the specified channel.")


@Client.on_message(filters.chat(-1001986761426) & (media_filter))
async def editing(bot, message):
    if message.from_user is None:
        return

    user_id = message.from_user.id
    channel_id = str(message.chat.id)
    if is_channel_added(channel_id):
        caption = get_caption(user_id, channel_id)

        try:
            media = message.document or message.video or message.audio
            caption_text = f"**{caption}**"
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
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=file_caption + "\n" + caption_text,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        except:
            pass
    else:
        await bot.send_message(-1001970089414, ChatMSG.NOT_FOUND_TXT.format(message.chat.title, message.chat.id))






            


