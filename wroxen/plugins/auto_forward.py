# (c) @TheLx0980


import logging
from pyrogram import Client, filters, enums
from wroxen.database.caption_db import set_forward_settings, delete_forward_settings, get_forward_settings, \
   clear_forward_db, update_forward_settings, add_replace_settings, delete_caption_settings, \
   delete_replace_settings, delete_replace_settings, add_caption
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
        await message.reply(f"Forwarding Successfully Set!\n\nFrom: {from_chat}\nTo Chat: {to_chat}")
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

    deleted_count = delete_forward_settings(channel_id)

    if deleted_count > 0:
        await message.reply(f"Forwarding settings for channel {channel_id} deleted.")
    else:
        await message.reply(f"No forwarding settings found for channel {channel_id}.")

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

        
@Client.on_message(filters.command("clearForwardDb"))
async def clear_forward_db_command(bot, message):
    delete_count = clear_forward_db()
    await message.reply(f"All forwarding connections deleted. Total deleted count: {delete_count}.")

# Command to update caption
@Client.on_message(filters.command("update_caption"))
async def update_caption_command(bot, message):
    if len(message.command) < 2:
        await bot.send_message(message.chat.id, "Please provide the new caption.")
        return

    new_caption = " ".join(message.command[1:])

    channel_id = str(message.chat.id)
    replace_settings = get_replace_settings(channel_id)
    if replace_settings:
        replace_settings["caption"] = new_caption
        caption_collection.update_one(
            {"channel_id": channel_id},
            {"$set": replace_settings},
            upsert=True
        )
        await bot.send_message(message.chat.id, f"Caption updated successfully.\n\nNew Caption: {new_caption}")
    else:
        await bot.send_message(message.chat.id, "Replace settings not found for the channel.")

# Command to update replace text
@Client.on_message(filters.command("update_replace_text"))
async def update_replace_text_command(bot, message):
    if len(message.command) < 3:
        await bot.send_message(message.chat.id, "Invalid command. Usage: /update_replace_text <old_username> <new_username>")
        return

    channel_id = str(message.chat.id)
    old_username = message.command[1]
    new_username = message.command[2]

    replace_settings = get_replace_settings(channel_id)
    if replace_settings:
        replace_settings["old_username"] = old_username
        replace_settings["new_username"] = new_username
        caption_collection.update_one(
            {"channel_id": channel_id},
            {"$set": replace_settings},
            upsert=True
        )
        await bot.send_message(message.chat.id, f"Replace text updated successfully.\n\nOld Username: {old_username}\nNew Username: {new_username}")
    else:
        await bot.send_message(message.chat.id, "Replace settings not found for the channel.")





