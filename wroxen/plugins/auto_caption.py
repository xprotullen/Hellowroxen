# (c) @thelx0980

from wroxen.database.authorized_chat import get_authorized_channels
from pyrogram.errors import FloodWait
from wroxen.chek import is_channel_added
from wroxen.text import ChatMSG
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums
from wroxen.wroxen import Wroxen
from wroxen.database.caption_db import add_channel, delete_channel, get_caption, channels_collection, \
    update_caption, get_forward_settings, get_replace_data

import logging, asyncio

media_filter = filters.document | filters.video | filters.audio
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("update_caption"))
async def update_caption_command(bot, message):
    channel_id = str(message.chat.id)
  
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/update_caption {new_caption}`.")
        return

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


@Client.on_message(filters.command("caption") & filters.channel)
async def get_caption_command(bot, message):
    channel_id = str(message.chat.id)
    authorised = get_authorized_channels(channel_id)

    if channel_id not in authorised:
        await message.reply("Your channel is not authorized to execute this command.")
        return

    caption = get_caption(channel_id)

    if caption:
        await message.reply(f"The caption for channel {channel_id} is:\n{caption}")
    else:
        await message.reply(f"No caption found for channel {channel_id}.")


@Client.on_message(filters.command("set_caption"))
async def set_caption_command(bot, message):
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/set_caption {caption}`.")
        return

    channel_id = str(message.chat.id)
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

    channel_id = str(message.chat.id)

    deleted = delete_channel(channel_id)
    if deleted:
        await message.reply(f"Caption deleted for channel {channel_id}.")
    else:
        await message.reply("No caption found for the specified channel.")


@Client.on_message(filters.channel & (media_filter))
async def editing(bot, message):
    channel_id = str(message.chat.id)
    if is_channel_added(channel_id):
        caption = get_caption(channel_id)
    
        try:
            media = message.document or message.video or message.audio
            caption_text = f"**{caption}**"
        except:
            caption_text = ""
            pass

        if message.document or message.video or message.audio:
            if message.caption:
                file_caption = f"**{message.caption}**"
            else:
                fname = media.file_name
                filename = fname.replace("_", ".")
                file_caption = f"`{filename}`"

        old_message_id = message.id

        if caption_text:
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=file_caption + "\n\n" + caption_text,
                parse_mode=enums.ParseMode.MARKDOWN
            )
    channel_id = str(message.chat.id)
    forward_settings = get_forward_settings(channel_id)
    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]
        old_username, new_username, caption = get_replace_data(channel_id)
        await bot.send_message(message.chat.id, f"New Username: {new_username}\nOld Username: {old_username}\nCaption: {caption}🖐️")
        if str(message.chat.id) == str(from_chat):
            try:
                new_caption = message.caption
                if caption:
                    new_caption = f"{new_caption}\n\n{caption}"
                if old_username and new_username and new_caption:
                    new_caption = new_caption.replace(old_username, new_username)

                await bot.copy_message(
                    chat_id=int(to_chat),
                    from_chat_id=message.chat.id,
                    message_id=message.id,
                    caption=new_caption,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            except Exception as e:
                print(f"Error copying message: {e}")




JAAN = """
@Client.on_message(filters.channel & (media_filter))
async def editing(bot, message):
    channel_id = str(message.chat.id)
    forward_settings = get_forward_settings(channel_id)
    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]
        old_username, new_username, caption = get_replace_data(channel_id)
        await bot.send_message(message.chat.id, f"New Username: {new_username}\nOld UserName {old_username}\ncaption: {caption}🖐️")
        if str(message.chat.id) == str(from_chat):
            try:
                new_caption = message.caption
                if caption:
                    new_caption = f"{new_caption}\n\n{caption}"
                if old_username and new_username and new_caption:
                    new_caption = new_caption.replace(old_username, new_username)

                await bot.copy_message(
                    chat_id=int(to_chat),
                    from_chat_id=message.chat.id,
                    message_id=message.id,
                    caption=new_caption,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error forwarding message: {e}")
    else:
        await bot.send_message(-1001970089414, f"Chat ID {channel_id} not found in forward settings.")


"""



            


