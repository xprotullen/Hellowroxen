# (c) @TheLx0980
# Year : 2023

import re
from bot.database.search_msg_db import get_channel_id
from pyrogram.types import Message, CallbackQuery
from wroxen.wroxen import Wroxen as Bot
from pyrogram import filters, Client
from wroxen.chek.search_caption_info import send_result_message, extract_movie_details, DATABASE
from html import escape

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

MEDIA_FILTER = enums.MessagesFilter.VIDEO

@Client.on_message(filters.group & filters.text)
async def filter(client: Client, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if len(message.text) > 2:
        query = message.text        
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
            await query.answer("Thats not for you!!",show_alert=True)
    
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
            await query.answer("Thats not for you!!",show_alert=True)
