# @thelx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums
from wroxen.wroxen import Wroxen
from wroxen.database.caption_db import set_caption, delete_caption, get_caption
import logging

media_filter = filters.document | filters.video | filters.audio
logger = logging.getLogger(__name__)

user_states = {}


@Client.on_message(filters.command("set_caption"))
async def set_caption_command(bot, message):
    user_id = message.from_user.id
    user_states[user_id] = {"step": 0, "channel_id": None, "caption": None}

    await message.reply("Send your channel ID:")
    user_states[user_id]["step"] = 1

@Client.on_message(filters.private & ~filters.command)
async def handle_private_message(bot, message):
    user_id = message.from_user.id

    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state["step"] == 1:
        state["channel_id"] = message.text
        await message.reply("Your channel ID has been recorded. Now send your channel caption:")
        state["step"] = 2
    elif state["step"] == 2:
        state["caption"] = message.text
        channel_id = state["channel_id"]
        caption = state["caption"]
        set_caption(user_id, channel_id, caption)
        await message.reply(f"Your caption `{caption}` has been set for channel `{channel_id}`.")
        del user_states[user_id]

    
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
    channel_id = message.chat.id
    if message.from_user is None:
        return

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

