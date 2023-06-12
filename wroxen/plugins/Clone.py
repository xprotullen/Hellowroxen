# (c)  @Hansaka_Anuhas | @TheLx0980

import asyncio
import re
from wroxen.vars import LOGGER
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# from wroxen.database.authorized_chat import get_authorized_channels
import logging
from wroxen.database import AuthorizedChannels

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

auth = AuthorizedChannels

CURRENT = {}
CHANNEL = {}
CANCEL = {}
FORWARDING = {}
CAPTION = {}

FILE_CAPTION = "{file_name}"



@Client.on_callback_query(filters.regex(r'^forward'))
async def forward(bot, query: CallbackQuery):
    _, ident, chat, lst_msg_id = query.data.split("#")
    if ident == 'yes':
        if FORWARDING.get(query.from_user.id):
            return await query.answer('पिछली प्रक्रिया पूरी होने तक प्रतीक्षा करें।', show_alert=True)

        msg = query.message
        await msg.edit('फ़ॉरवर्डिंग शुरू हो रही है...')
        try:
            chat = int(chat)
        except:
            chat = chat
        await forward_files(int(lst_msg_id), chat, msg, bot, query.from_user.id)

    elif ident == 'close':
        await query.answer("ठीक है!")
        await query.message.delete()

    elif ident == 'cancel':
        await query.message.edit("फ़ॉरवर्डिंग रद्द करने का प्रयास कर रहा है...")
        CANCEL[query.from_user.id] = True


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text) & filters.private & filters.incoming)
async def send_for_forward(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('फ़ॉरवर्ड करने के लिए अमान्य लिंक!')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return

    try:
        source_chat = await bot.get_chat(chat_id)
    except Exception as e:
        return await message.reply(f'त्रुटि - {e}')

    if source_chat.type != enums.ChatType.CHANNEL:
        return await message.reply("मैं केवल चैनल को फ़ॉरवर्ड कर सकता हूँ.")

    target_chat_id = CHANNEL.get(message.from_user.id)
    if not target_chat_id:
        return await message.reply("आपने लक्षित चैनल जोड़ा नहीं है।\n/clone_set_channel कमांड का उपयोग करके जोड़ें.")

    try:
        target_chat = await bot.get_chat(target_chat_id)
    except Exception as e:
        return await message.reply(f'त्रुटि - {e}')

    skip = CURRENT.get(message.from_user.id)
    if skip:
        skip = skip
    else:
        skip = 0
   
    caption = CAPTION.get(message.from_user.id)
    if caption:
        caption = caption
    else:
        caption = FILE_CAPTION
    # last_msg_id is same to total messages
    buttons = [[
        InlineKeyboardButton('हाँ', callback_data=f'forward#yes#{chat_id}#{last_msg_id}')
    ],[
        InlineKeyboardButton('बंद करें', callback_data=f'forward#close#{chat_id}#{last_msg_id}')
    ]]
    await message.reply(f"स्रोत चैनल: {source_chat.title}\nलक्षित चैनल: {target_chat.title}\nसंदेश छोड़ें: <code>{skip}</code>\nकुल संदेश: <code>{last_msg_id}</code>\nफ़ाइल कैप्शन: {caption}\n\nक्या आप फ़ॉरवर्ड करना चाहते हैं?", reply_markup=InlineKeyboardMarkup(buttons))
    
    
@Client.on_message(filters.private & filters.command(['set_clone_skip']))
async def set_skip_number(bot, message):
    target_chat_id = CHANNEL.get(message.from_user.id)
    if not target_chat_id:
        await message.reply("आपने लक्षित चैनल जोड़ा नहीं है।\n/clone_set_channel कमांड का उपयोग करके जोड़ें.")
        return
    try:
        _, skip = message.text.split(" ")
    except:
        return await message.reply("मुझे एक स्किप नंबर दें।")
    try:
        skip = int(skip)
    except:
        return await message.reply("केवल संख्याओं का समर्थन करें।")
    CURRENT[message.from_user.id] = int(skip)
    await message.reply(f"सफलतापूर्वक सेट किया गया है <code>{skip}</code> स्किप नंबर।")


@Client.on_message(filters.private & filters.command(['set_target_channel']))
async def set_target_channel(bot, message):
    try:
        _, chat_id = message.text.split(" ")
    except:
        return await message.reply("कृपया एक टारगेट चैनल ID दें।")
    try:
        chat_id = int(chat_id)
    except:
        return await message.reply("कृपया एक वैध ID दें।")

    try:
        chat = await bot.get_chat(chat_id)
    except:
        return await message.reply("मुझे अपने टारगेट चैनल में एडमिन बनाएं।")
    channel_id = str(chat.id)
    authorised = auth.get_authorized_channels(channel_id)
    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply("मैं केवल चैनल्स को सेट कर सकता हूँ।")
    if channel_id not in authorised:
        return await message.reply("आपका चैनल इस आदेश का उपयोग करने के लिए अधिकृत नहीं है।")
    CHANNEL[message.from_user.id] = int(chat.id)
    await message.reply(f"सफलतापूर्वक {chat.title} टारगेट चैनल सेट किया गया है।")


@Client.on_message(filters.private & filters.command(['set_clone_caption']))
async def set_caption(bot, message):
    target_chat_id = CHANNEL.get(message.from_user.id)
    if not target_chat_id:
        await message.reply("आपने लक्षित चैनल जोड़ा नहीं है।\n/clone_set_channel कमांड का उपयोग करके जोड़ें.")
        return
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply("मुझे एक कैप्शन दें।")
    CAPTION[message.from_user.id] = caption
    await message.reply(f"सफलतापूर्वक फ़ाइल कैप्शन सेट किया गया है।\n\n{caption}")
    
    
    
async def forward_files(lst_msg_id, chat, msg, bot, user_id):
    current = CURRENT.get(user_id) if CURRENT.get(user_id) else 0
    forwarded = 0
    deleted = 0
    unsupported = 0
    fetched = 0
    CANCEL[user_id] = False
    FORWARDING[user_id] = True
    # lst_msg_id is same to total messages

    try:
        async for message in bot.iter_messages(chat, lst_msg_id, CURRENT.get(user_id) if CURRENT.get(user_id) else 0):
            if CANCEL.get(user_id):
                await msg.edit(f"फ़ॉरवर्ड सफलतापूर्वक रद्द किया गया!")
                break
            current += 1
            fetched += 1
            if current % 20 == 0:
                btn = [[
                    InlineKeyboardButton('रद्द करें', callback_data=f'forward#cancel#{chat}#{lst_msg_id}')
                ]]
                await msg.edit_text(text=f"फ़ॉरवर्ड प्रसंस्करण हो रहा है...\n\nकुल संदेश: <code>{lst_msg_id}</code>\nपूरे किए गए संदेश: <code>{current} / {lst_msg_id}</code>\nफ़ाइल फ़ॉरवर्ड की गई: <code>{forwarded}</code>\nहटाए गए संदेश छोड़े: <code>{deleted}</code>\nअसमर्थित फ़ाइलें छोड़ी गई: <code>{unsupported}</code>", reply_markup=InlineKeyboardMarkup(btn))
            if message.empty:
                deleted += 1
                continue
            elif not message.media:
                unsupported += 1
                continue
            elif message.media not in [enums.MessageMediaType.DOCUMENT, enums.MessageMediaType.VIDEO]:  # Non documents and videos files skipping
                unsupported += 1
                continue
            media = getattr(message, message.media.value, None)
            if not media:
                unsupported += 1
                continue
            elif media.mime_type not in ['video/mp4', 'video/x-matroska']:  # Non mp4 and mkv files types skipping
                unsupported += 1
                continue
            try:
                await bot.send_cached_media(
                    chat_id=CHANNEL.get(user_id),
                    file_id=media.file_id,
                    caption=CAPTION.get(user_id).format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption) if CAPTION.get(user_id) else FILE_CAPTION.format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption)
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)  # Wait "value" seconds before continuing
                await bot.send_cached_media(
                    chat_id=CHANNEL.get(user_id),
                    file_id=media.file_id,
                    caption=CAPTION.get(user_id).format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption) if CAPTION.get(user_id) else FILE_CAPTION.format(file_name=media.file_name, file_size=get_size(media.file_size), caption=message.caption)
                )
            forwarded += 1
            await asyncio.sleep(1)
    except Exception as e:
        logger.exception(e)
        await msg.reply(f"फ़ॉरवर्ड रद्द किया गया!\n\nत्रुटि - {e}")
    else:
        await msg.edit(f'फ़ॉरवर्ड पूर्ण हुआ!\n\nकुल संदेश: <code>{lst_msg_id}</code>\nपूरे किए गए संदेश: <code>{current} / {lst_msg_id}</code>\nप्राप्त किए गए संदेश: <code>{fetched}</code>\nकुल फ़ॉरवर्ड की गई फ़ाइलें: <code>{forwarded}</code>\nहटाए गए संदेश छोड़े: <code>{deleted}</code>\nअसमर्थित फ़ाइलें छोड़ी गई: <code>{unsupported}</code>')
        FORWARDING[user_id] = False


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
