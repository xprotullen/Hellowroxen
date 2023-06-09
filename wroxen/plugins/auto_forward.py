# (c) @TheLx0980


import logging
from pyrogram import Client, filters, enums
from wroxen.database.caption_db import set_forward_settings, delete_forward_settings, get_forward_settings
  
logger = logging.getLogger(__name__)
media_filter = filters.document | filters.video

@Client.on_message(filters.command("set_forward"))
async def set_forward_command(bot, message):
    command_parts = message.text.split(" ", 3)

    if len(command_parts) != 3:
        await message.reply("Invalid format. Please use the format `/set_forward {from_chat} {to_chat}`.")
        return

    from_chat = command_parts[1]
    to_chat = command_parts[2]

    if not from_chat.startswith("-100"):
        from_chat = "-100" + from_chat

    if not to_chat.startswith("-100"):
        to_chat = "-100" + to_chat

    try:
        set_forward_settings(from_chat, to_chat)
        await message.reply("Forwarding Successfully Set!\n\nFrom: {from_chat}\nTo Chat: {to_chat}")                         
    except ValueError as e:
        await message.reply(str(e))
        
@Client.on_message(filters.command("delete_forward"))
async def delete_forward_command(bot, message):
    command_parts = message.text.split(" ", 2)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/delete_forward {channel_id}`.")
        return

    channel_id = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    delete_forward_settings(channel_id)
    await message.reply("Forwarding settings deleted.")

@Client.on_message(filters.command("check_forward"))
async def check_forward_command(bot, message):
    command_parts = message.text.split(" ", 2)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/check_forward {channel_id}`.")
        return

    channel_id = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    forward_settings = get_forward_settings(channel_id)

    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]
        await message.reply(f"Forwarding settings:\nFrom Channel: {from_chat}\nTo Channel: {to_chat}")
    else:
        await message.reply("Forwarding settings not found.")
