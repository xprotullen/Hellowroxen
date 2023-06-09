# (c) @TheLx0980


import logging
from pyrogram import Client, filters, enums
from wroxen.database.autoforward_db import set_forward_settings, get_forward_settings
  
logger = logging.getLogger(__name__)
media_filter = filters.document | filters.video

@Client.on_message(filters.command("AutoForward"))
async def set_forward_command(bot, message):
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("Invalid format. Please use the format `/AutoForward {to_chat}`.")
        return

    to_chat = command_parts[1]
    if not to_chat.startswith("-100"):
        to_chat = "-100" + to_chat

    from_chat = message.chat.id

    try:
        set_forward_settings(from_chat, to_chat)
        await message.reply("Auto forwarding settings updated.")
    except:
        await message.reply("Failed to update auto forwarding settings.")

HELLO = """
@Client.on_message(filters.channel & media_filter)
async def forward(bot, update):
    forward_settings = get_forward_settings()

    if forward_settings:
        from_chat = forward_settings["from_chat"]
        to_chat = forward_settings["to_chat"]

        if to_chat.startswith("-100"):
            to_chat = to_chat[4:]

        if str(update.chat.id) == from_chat:
            try:
                await bot.copy_message(
                    chat_id=int(to_chat),
                    from_chat_id=update.chat.id,
                    message_id=update.message_id,
                    caption=f"**{update.caption}**",
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)S
"""
