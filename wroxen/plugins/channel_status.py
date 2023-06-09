# (c) @TheLx0980

from wroxen.database.caption_db import get_forward_settings, get_replace_data
from pyrogram import Client, filters

@Client.on_message(filters.command("Channel_status") & filters.channel)
async def channel_status_command(bot, message):
    channel_id = str(message.chat.id)
    forward_settings = get_forward_settings(channel_id)
    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]
        caption, old_username, new_username = get_replace_data(channel_id)
        
        channel_status_text = f"From Channel: {from_chat}\nTo Channel: {to_chat}\n\n"
        channel_status_text += f"Replace txt: {old_username} => {new_username}\n\n"
        channel_status_text += f"Caption: {caption}\n\n"
        channel_status_text += f"Channel name: {message.chat.title}"

        await bot.send_message(message.chat.id, channel_status_text)
    else:
        await bot.send_message(message.chat.id, f"Forward settings not found for Channel ID {channel_id}")
