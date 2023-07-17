# (c) @TheLx0980

from wroxen.database import Database, AuthorizedChannels
import logging
from pyrogram import Client, filters, enums
from wroxen.vars import ADMIN_IDS
logger = logging.getLogger(__name__)

db = Database()
auth = AuthorizedChannels

@Client.on_message(filters.command("set_forward") & filters.channel)
async def set_forward_command(bot, message):
    channel_id = str(message.chat.id)
    authorised = auth.get_authorized_channels(channel_id)

    if channel_id not in authorised:
        await message.reply("आपका चैनल इस आदेश को निष्पादित करने के लिए अधिकृत नहीं है।")
        return
    
    command_parts = message.text.split(" ", 2)

    if len(command_parts) != 2:
        await message.reply("अमान्य प्रारूप। कृपया इस प्रारूप का उपयोग करें: `/set_forward {to_chat}`।")
        return

    from_chat = str(message.chat.id)
    to_chat = command_parts[1]

    if not to_chat.startswith("-100"):
        to_chat = "-100" + to_chat

    try:
        db.set_forward_settings(from_chat, to_chat)
        await message.reply(f"फ़ोरवर्डिंग सफलतापूर्वक सेट की गई!\n\nसे: {from_chat}\nटू चैट: {to_chat}")
    except ValueError as e:
        await message.reply(str(e))

        
@Client.on_message(filters.command("delete_forward") & filters.channel)
async def delete_forward_command(bot, message):
    channel_id = str(message.chat.id)

    deleted_count = db.delete_forward_settings(channel_id)

    if deleted_count > 0:
        await message.reply(f"चैनल {channel_id} के लिए फ़ोरवर्डिंग सेटिंग्स हटा दी गईं।")
    else:
        await message.reply(f"चैनल {channel_id} के लिए कोई फ़ोरवर्डिंग सेटिंग्स नहीं मिलीं।")

        
@Client.on_message(filters.command("clearForwardDb") & filters.private)
async def clear_forward_db_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आप इस आदेश को निष्पादित करने के लिए अधिकृत उपयोगकर्ता नहीं हैं।")
        return
    delete_count = db.clear_forward_db()
    await message.reply(f"सभी फवार्डिंग कनेक्शन हटा दिए गए। कुल हटाए गए काउंट: {delete_count}.")
      

@Client.on_message(filters.command("add_f_caption_info") & filters.channel)
async def add_f_caption_info_command(bot, message):
    channel_id = str(message.chat.id)
    authorised = auth.get_authorized_channels(channel_id)

    if channel_id not in authorised:
        await message.reply("आपका चैनल इस आदेश को निष्पादित करने के लिए अधिकृत नहीं है।")
        return
    if len(message.command) < 4:
        await bot.send_message(message.chat.id, "अमान्य कमांड। उपयोग: /add_f_caption {पुराना_यूज़रनेम} {नया_यूज़रनेम} {कैप्शन}")
        return

    command_args = message.command[1:]
    old_username = command_args[0]
    new_username = command_args[1]
    caption = " ".join(command_args[2:])
    
    try:
        db.add_replace_settings(channel_id, old_username, new_username, caption)
        await bot.send_message(message.chat.id, f"कैप्शन सफलतापूर्वक जोड़ा गया।\n<b>कैप्शन:</b> <code>{caption}</code>\n<b>बदलना:</b> <code>{old_username}</code>\n<b>बदलना जाएगा:</b> <code>{new_username}</code>") 
    except ValueError as e:
        await bot.send_message(message.chat.id, str(e))



  
@Client.on_message(filters.command("update_f_caption") & filters.channel)
async def update_caption_command(bot, message):
    if len(message.command) < 2:
        await bot.send_message(message.chat.id, "कृपया नया कैप्शन प्रदान करें।")
        return

    new_caption = " ".join(message.command[1:])

    channel_id = str(message.chat.id)
    if db.update_f_caption(channel_id, new_caption):
        await bot.send_message(message.chat.id, f"कैप्शन सफलतापूर्वक अपडेट किया गया।\n\nनया कैप्शन: {new_caption}")
    else:
        await bot.send_message(message.chat.id, "चैनल के लिए प्रतिस्थापन सेटिंग नहीं मिली।")

# टेक्स्ट को अपडेट करने की कमांड
@Client.on_message(filters.command("update_replace_text") & filters.channel)
async def update_replace_text_command(bot, message):
    if len(message.command) < 3:
        await bot.send_message(message.chat.id, "अमान्य आदेश। उपयोग: /update_replace_text <old_username> <new_username>")
        return

    channel_id = str(message.chat.id)
    old_username = message.command[1]
    new_username = message.command[2]

    if db.update_replace_text(channel_id, old_username, new_username):
        await bot.send_message(message.chat.id, f"प्रतिस्थापित पाठ सफलतापूर्वक अपडेट किया गया।\n\nपुराना उपयोगकर्ता नाम: {old_username}\nनया उपयोगकर्ता नाम: {new_username}")
    else:
        await bot.send_message(message.chat.id, "चैनल के लिए प्रतिस्थापित सेटिंग नहीं मिली।")

@Client.on_message(filters.command("delete_f_caption") & filters.channel)
async def delete_caption_command(bot, message):
    channel_id = str(message.chat.id)
    
    try:
        db.delete_caption_settings(channel_id)
        await bot.send_message(message.chat.id, "Caption deleted from replace settings.")
    except ValueError as e:
        await bot.send_message(message.chat.id, str(e))

         
@Client.on_message(filters.command("delete_replace") & filters.channel)
async def delete_replace_command(bot, message):
    channel_id = str(message.chat.id)
    forward_settings = db.get_forward_settings(channel_id)
    if forward_settings:
        old_username, new_username, _ = auth.get_replace_data(channel_id)
        if old_username and new_username:
            db.delete_replace_settings(channel_id, old_username, new_username)
            await bot.send_message(message.chat.id, "Replace settings deleted successfully.")
        else:
            await bot.send_message(message.chat.id, "इस चैनल के लिए सेटिंग बदलें (बदलना) मौजूद नहीं है")
    else:
        await bot.send_message(message.chat.id, f"Forward settings not found for Channel ID {channel_id}")



@Client.on_message(filters.command("add_f_replace") & filters.channel)
async def add_f_replace_command(bot, message):
     channel_id = str(message.chat.id)
     authorised = auth.get_authorized_channels(channel_id)
     
     if channel_id not in authorised:
         await message.reply("आपका चैनल इस आदेश को निष्पादित करने के लिए अधिकृत नहीं है।")
         return
     if len(message.command) < 2:
          await bot.send_message(message.chat.id, "अवैध आदेश।  प्रयोग: /add_f_replace {old_username} {new_username}")
          return

     command_args = message.command[1:]
     if len(command_args) != 2:
         await bot.send_message(message.chat.id, "अवैध आदेश।  प्रयोग: /add_f_replace {old_username} {new_username}")
         return

     old_username = command_args[0]
     new_username = command_args[1]

     channel_id = str(message.chat.id)

     try:
         db.add_replace_settings(channel_id, old_username, new_username, "")
         await bot.send_message(message.chat.id, "Username replaced successfully.")
     except ValueError as e:
         await bot.send_message(message.chat.id, str(e))

@Client.on_message(filters.command("Add_f_caption") & filters.channel)
async def add_f_caption_command(bot, message):
    channel_id = str(message.chat.id)
    authorised = auth.get_authorized_channels(channel_id)

    if channel_id not in authorised:
        await message.reply("आपका चैनल इस आदेश को निष्पादित करने के लिए अधिकृत नहीं है।")
        return   
    if message.reply_to_message is None:
        await bot.send_message(message.chat.id, "कृपया इस आदेश का उपयोग करते समय संदेश का उत्तर दें।")
        return

    channel_id = str(message.chat.id)
    reply_message = message.reply_to_message
    caption = reply_message.caption if reply_message.caption else ""

    try:
        db.add_replace_settings(channel_id, "", "", caption)
        await bot.send_message(message.chat.id, "कैप्शन सफलतापूर्वक जोड़ा गया।")
    except ValueError as e:
        await bot.send_message(message.chat.id, str(e))


@Client.on_message(filters.command("delete_f_captions") & filters.channel)
async def delete_f_captions_command(bot, message):
    channel_id = str(message.chat.id)

    result = db.caption_collection.delete_many({"channel_id": channel_id})

    if result.deleted_count > 0:
        await bot.send_message(message.chat.id, f"चैनल आईडी {channel_id} के लिए सभी कैप्शन सफलतापूर्वक हटा दिए गए हैं।")
    else:
        await bot.send_message(message.chat.id, f"चैनल आईडी के लिए कोई कैप्शन नहीं मिला। {channel_id}.")
         
         
         
         
         
         
         
         
         
