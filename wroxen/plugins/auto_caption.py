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
from wroxen.vars import ADMIN_IDS
import logging, asyncio

media_filter = filters.document | filters.video | filters.audio
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("update_caption") & filters.channel)
async def update_caption_command(bot, message):
    channel_id = str(message.chat.id)
  
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("अवैध प्रारूप।  कृपया सही प्रारूप का उपयोग करें`/update_caption {new_caption}`.")
        return

    new_caption = command_parts[1]
    
    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    if not is_channel_added(channel_id):
        await message.reply("इस चैनल को डेटाबेस में नहीं जोड़ा गया है।")
        return

    try:
        update_caption(channel_id, new_caption)
        await message.reply(f"चैनल {channel_id} के लिए कैप्शन अपडेट किया गया।\n\n{new_caption}")
    except ValueError:
        await message.reply("डेटाबेस में कैप्शन अपडेट करते समय एक त्रुटि हुई। ")


@Client.on_message(filters.command("caption") & filters.channel)
async def get_caption_command(bot, message):
    channel_id = str(message.chat.id)
    authorised = get_authorized_channels(channel_id)

    if channel_id not in authorised:
        await message.reply("आपका चैनल इस आदेश को निष्पादित करने के लिए अधिकृत नहीं है।")
        return

    caption = get_caption(channel_id)

    if caption:
        await message.reply(f"{channel_id} इस चैनल के लिए कैप्शन सेट किया गया।\nकैप्शन{caption}")
    else:
        await message.reply(f"इस चैनल के लिए कोई कैप्शन नहीं मिला {channel_id}.")


@Client.on_message(filters.command("set_caption") & filters.channel)
async def set_caption_command(bot, message):
    channel_id = str(message.chat.id)
    authorized_channels = get_authorized_channels(channel_id)
    
    if channel_id not in authorized_channels:
        await message.reply("आपका चैनल इस आदेश को निष्पादित करने के लिए अधिकृत नहीं है।")
        return
    
    command_parts = message.text.split(" ", 1)

    if len(command_parts) != 2:
        await message.reply("अवैध प्रारूप।  कृपया सही  प्रारूप का उपयोग करें `/set_caption {caption}`.")
        return

    caption = command_parts[1]

    if not channel_id.startswith("-100"):
        channel_id = "-100" + channel_id

    try:
        add_channel(channel_id, caption)
        await message.reply(f"चैनल के लिए कैप्शन सेट किया {channel_id}.\n\n{caption}")
    except ValueError:
        await message.reply("चैनल पहले ही डेटाबेस में जोड़ा जा चुका है!")


@Client.on_message(filters.command("ClearCaptionDB") & filters.private)
async def delete_all_info_command(bot, message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("आपको इस आदेश का उपयोग करने का अधिकार नहीं है।")
        return

    confirmation_message = "क्या आप वाकई सभी ऑटो कैप्शन जानकारी को हटाना चाहते हैं? यह कार्रवाई पूर्ववत नहीं की जा सकती है।\n\nकृपया पुष्टि के लिए 'हाँ' के साथ जवाब दें।"
    await message.reply(confirmation_message)

    try:
        response = await bot.wait_for("message", timeout=30, chat_id=message.from_user.id)
        if response.text.lower() == "हाँ":
            channels_collection.delete_many({})
            await message.reply("डेटाबेस की सभी ऑटो कैप्शन जानकारी को सफलतापूर्वक हटा दिया गया है।")
        else:
            await message.reply("ऑटो कैप्शन हटाना रद्द कर दिया गया है।")
    except asyncio.TimeoutError:
        await message.reply("ऑटो कैप्शन हटाने का समय समाप्त हो गया है। कृपया पुन: प्रयास करें।")


@Client.on_message(filters.command("delete_caption") & filters.channel)
async def delete_caption_command(bot, message):

    channel_id = str(message.chat.id)

    deleted = delete_channel(channel_id)
    if deleted:
        await message.reply(f"{channel_id} इस चैनल के लिए कैप्शन हटाया गया।")
    else:
        await message.reply("आप जिस चैनल की कैप्शन को हटाने की कोशिश कर रहे हैं उसके लिए कोई कैप्शन नहीं मिला।")


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










            


