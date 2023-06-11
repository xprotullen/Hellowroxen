# (c) @TheLx0980

import asyncio
from wroxen.database.authorized_chat import get_authorized_channels, add_authorized_channel, delete_authorized_channel, \
   delete_all_authorized_chats, get_authorized_chat
from wroxen.database.caption_db import get_forward_settings, get_replace_data, clear_all_db, get_caption
from pyrogram import Client, filters
from wroxen.vars import ADMIN_IDS

# AUTHORIZED_CHANL = get_authorized_channels()
delete_confirmation = {}

@Client.on_message(filters.command("Channel_status") & filters.channel)
async def channel_status_command(bot, message):
    channel_id = str(message.chat.id)
    auto_caption = get_caption(channel_id)
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

Channel Auto Caption:
{auto_caption}

Channel name: {message.chat.title}"""

        await bot.send_message(message.chat.id, channel_status_text)
    else:
        await bot.send_message(message.chat.id, f"चैनल आईडी के लिए अग्रेषण सेटिंग नहीं मिलीं {channel_id}")


        

@Client.on_message(filters.command("add_authorised_chat") & filters.private)
async def add_authorised_chat_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आप इस आदेश को निष्पादित करने के लिए अधिकृत उपयोगकर्ता नहीं हैं")
        return

    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("अवैध प्रारूप।  कृपया सही प्रारूप का उपयोग करें`/add_authorised_chat {channel_id}`.")
        return

    channel_id = command_parts[1]
    
    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id
    
    authorized_chat = get_authorized_channels(channel_id)
    
    if channel_id in authorized_chat:
        await message.reply("चैनल आईडी पहले से ही अधिकृत है।")
        return

    try:
        add_authorized_channel(channel_id)
        await message.reply(f"Channel ID {channel_id} अधिकृत सूची में जोड़ा गया।")
    except Exception as e:
        await message.reply("अधिकृत सूची में चैनल आईडी जोड़ते समय एक त्रुटि हुई।")


@Client.on_message(filters.command("delete_authorised_chat") & filters.private)
async def delete_authorised_chat_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आप इस आदेश को निष्पादित करने के लिए अधिकृत उपयोगकर्ता नहीं हैं।")
        return

    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("अवैध प्रारूप।  कृपया सही प्रारूप का उपयोग करें `/delete_authorised_chat {channel_id}`.")
        return

    channel_id = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    try:
        delete_authorized_channel(channel_id)
        await message.reply(f"{channel_id} को अधिकृत सूची से हटा दिया गया।")
    except Exception as e:
        await message.reply("प्राधिकृत सूची से चैनल आईडी निकालते समय एक त्रुटि हुई।")

@Client.on_message(filters.command("delete_all_authorised_chats") & filters.private)
async def delete_all_authorised_chats_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आप इस आदेश को निष्पादित करने के लिए अधिकृत उपयोगकर्ता नहीं हैं")
        return

    try:
        deleted_count = delete_all_authorized_chats()
        await message.reply(f"{deleted_count} अधिकृत चैट हटा दी गई हैं।")
    except Exception as e:
        await message.reply("अधिकृत चैट को हटाते समय एक त्रुटि हुई")
        
        
        
@Client.on_message(filters.command("check_authorised") & filters.private)
async def check_authorised_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आप इस आदेश को निष्पादित करने के लिए अधिकृत उपयोगकर्ता नहीं हैं")
        return

    try:
        authorised_chats = get_authorized_chat()
        if not authorised_chats:
            await message.reply("कोई अधिकृत चैट नहीं मिली।")
        else:
            reply_message = "अधिकृत चैट:\n"
            for chat_id in authorised_chats:
                reply_message += f"- {chat_id}\n"
            await message.reply(reply_message)
    except Exception as e:
        await message.reply("An error occurred while checking the authorized chats.")


@Client.on_message(filters.command("clearalldb"))
async def clear_all_db_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आपको इस कमांड को निष्पादित करने के लिए अधिकृत उपयोगकर्ता नहीं हैं।")
        return
     
    command_msg = message.text.split(" ", 1)      
    yes_msg = command_msg[1]
    delete_count = clear_all_db()
    
    if "हाँ" == yes_msg:
        if delete_count > 0:
            await message.reply(f"आपका डेटाबेस हटा दिया गया है।\n\nकुल मिटाए गए दस्तावेज़ों की संख्या: {delete_count}")
        else:
            await message.reply("आपका डेटाबेस हटाने में असमर्थ रहा।")
    else:
        await message.reply("अमान्य कमांड प्रारूप: उपयोग करें\n\n <code>/ClearAllDb हाँ</code>")



        
