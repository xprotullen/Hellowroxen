# (c) @TheLx0980
# Year : 2023

import re
from wroxen.database.search_msg_db import get_channel_id, add_channel, delete_channel, is_group_in_database
from pyrogram.types import Message, CallbackQuery
from wroxen.wroxen import Wroxen as Bot
from pyrogram import filters, Client, enums
from wroxen.chek.search_caption_info import send_result_message, extract_movie_details, DATABASE
from html import escape

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

MEDIA_FILTER = enums.MessagesFilter.VIDEO


@Client.on_message(filters.command("add_search_cnl") & filters.reply)
async def add_channel_handler(client, message):
    chat_id = message.chat.id
    group_id = message.chat.id
    channel_id = message.reply_to_message.forward_from_chat.id

    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"आप एक अज्ञात व्यवस्थापक हैं।")

    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return

    st = await client.get_chat_member(chat_id, userid)
    if (
        st.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    ):
        return

    if is_group_in_database(group_id):
        if get_channel_id(group_id) == channel_id:
            await client.send_message(
                chat_id=chat_id,
                text="समूह के लिए चैनल आईडी पहले से ही जोड़ दिया गया है।"
            )
        else:
            add_channel(group_id, channel_id)
            await client.send_message(
                chat_id=chat_id,
                text="समूह के लिए चैनल आईडी अपडेट की गई है।"
            )
    else:
        add_channel(group_id, channel_id)
        await client.send_message(
            chat_id=chat_id,
            text="चैनल आईडी को डेटाबेस में जोड़ दिया गया है।"
        )
       

@Client.on_message(filters.command("delete_search_cnl") & filters.group)
async def delete_channel_handler(client, message):
    chat_id = message.chat.id
    group_id = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"आप एक अज्ञात व्यवस्थापक हैं।")

    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return

    st = await client.get_chat_member(chat_id, userid)
    if (
        st.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    ):
        return

    if is_group_in_database(group_id):
        delete_channel(group_id)
        await client.send_message(
            chat_id=chat_id,
            text="समूह और उससे संबंधित चैनल को डेटाबेस से हटा दिया गया है।"
        )
    else:
        await client.send_message(
            chat_id=chat_id,
            text="समूह डेटाबेस में मौजूद नहीं है।"
        )


@Client.on_message(filters.group & filters.text)
async def filter(client: Client, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if len(message.text) > 2:
        query = message.text
        group_id = message.chat.id
        channel_id = get_channel_id(group_id)

        if not channel_id:
            return
   
        msgs = []
        search_id = int(channel_id)
        async for msg in client.USER.search_messages(search_id, query=query, filter=MEDIA_FILTER):
            caption = msg.caption
            movie_name, year, quality = extract_movie_details(caption)
            link = msg.link                     
            movie_text = f"<b>{escape(movie_name)} ({year}) {quality}</b>\n<b>Link:</b> {link}"
            msgs.append(movie_text)

        if not msgs:
            return

        page = 1
        await send_result_message(client, message, query, msgs, page)

@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data
    
    if data.startswith('next_page:'):
        _, query_text, page = data.split(':')
        
        # Retrieve data from DATABASE
        db_entry = DATABASE.get(query_text)
        if db_entry:
            movies = db_entry['movies']
            result_message_id = db_entry['message_id']
            
            await query.answer()
            await send_result_message(client, query.message, query_text, movies, int(page), result_message_id)
        else:
            await query.answer("यह आपके लिए नहीं है!",show_alert=True)
    
    elif data.startswith('previous_page:'):
        _, query_text, page = data.split(':')
        
        # Retrieve data from DATABASE
        db_entry = DATABASE.get(query_text)
        if db_entry:
            movies = db_entry['movies']
            result_message_id = db_entry['message_id']
            
            await query.answer()
            await send_result_message(client, query.message, query_text, movies, int(page), result_message_id)
        else:
            await query.answer("यह आपके लिए नहीं है!",show_alert=True)
