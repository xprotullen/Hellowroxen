# (c) @TheLx0980

from wroxen.database.authorized_chat import get_authorized_channels, add_authorized_channel
from wroxen.database.caption_db import get_forward_settings, get_replace_data
from pyrogram import Client, filters

AUTHORIZED_CHANL = get_authorized_channels()

@Client.on_message(filters.command("Channel_status") & filters.channel)
async def channel_status_command(bot, message):
    channel_id = str(message.chat.id)
    forward_settings = get_forward_settings(channel_id)
    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]
        old_username, new_username, caption = get_replace_data(channel_id)
        await bot.send_message(message.chat.id, f"New Username: {new_username} 🖐️")
        channel_status_text = f"""
From Channel: {from_chat}
To chat: {to_chat}
        
Caption: {caption}
        
Replace TEXT:
{old_username} To {new_username}

Channel name: {message.chat.title}"""

        await bot.send_message(message.chat.id, channel_status_text)
    else:
        await bot.send_message(message.chat.id, f"Forward settings not found for Channel ID {channel_id}")


        

@Client.on_message(filters.command("add_authorised_chat"))
async def add_authorised_chat_command(bot, message):
    if message.from_user.id not in AUTHORIZED_USER_IDS:
        await message.reply("You are not an authorized user to execute this command.")
        return

    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/add_authorised_chat {channel_id}`.")
        return

    channel_id = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    if channel_id in AUTHORIZED_CHANL:
        await message.reply("Channel ID is already authorized.")
        return

    try:
        add_authorized_channel(channel_id)
        AUTHORIZED_CHANL.append(channel_id)
        await message.reply(f"Channel ID {channel_id} added to authorized list.")
    except Exception as e:
        await message.reply("An error occurred while adding the channel ID to the authorized list.")
