# (c) @TheLx0980
# Year : 2023

import re, pyrogram
from pyrogram import filters, enums, Client
from wroxen.wroxen import Wroxen as Bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import logging
from wroxen.database.search_msg_db import get_channel_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

MEDIA_FILTER = enums.MessagesFilter.VIDEO 
BUTTONS = {}
DATABASE = {}

from html import escape



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
            file_name = msg.caption
            link = msg.link
            movie_text = f"<b>{file_name}</b>\nLink: {link}"
            msgs.append(movie_text)

        if not msgs:
            return

        page = 1
        await send_result_message(client, message, query, msgs, page)


async def send_result_message(client, message, query, movies, page, result_message_id=None):
    total_results = len(movies)

    if total_results <= 10:
        # Less than or equal to 10 results, no need for pagination
        movies_page = movies
        reply_markup = None
    else:
        results_per_page = 10
        start_index = (page - 1) * results_per_page
        end_index = page * results_per_page
        movies_page = movies[start_index:end_index]
        reply_markup = generate_inline_keyboard(query, total_results, page)

    result_message = generate_result_message(query, movies_page, page)

    if result_message_id:
        # Edit the existing message
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=result_message_id,
            text=result_message,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        # Send a new message
        sent_message = await message.reply_text(
            result_message,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )
        result_message_id = sent_message.id

    DATABASE[query] = {
        'message_id': result_message_id,
        'movies': movies,
        'page': page
    }





def generate_inline_keyboard(query, total_results, current_page):
    buttons = []

    if total_results > current_page * 10:
        next_page_button = InlineKeyboardButton(
            text='Next Page',
            callback_data=f'next_page:{query}:{current_page + 1}'
        )
        buttons.append(next_page_button)

    if current_page > 1:
        previous_page_button = InlineKeyboardButton(
            text='Previous Page',
            callback_data=f'previous_page:{query}:{current_page - 1}'
        )
        buttons.append(previous_page_button)

    inline_keyboard = [buttons]
    return InlineKeyboardMarkup(inline_keyboard) 


def generate_result_message(query, movies, page):
    start_number = (page - 1) * 10 + 1
    result_message = f"Here are the results for <b>{escape(query)}</b>:\n\n"
    for i, movie_text in enumerate(movies, start=start_number):
        result_message += f"{i}. {movie_text}\n\n"
    return result_message


@Client.on_callback_query(filters.regex(r'^next_page:'))
async def next_page_callback(client: Client, query: CallbackQuery):
    data = query.data
    _, query_text, page = data.split(':')
        
    # Retrieve data from DATABASE
    db_entry = DATABASE.get(query_text)
    if db_entry:
        movies = db_entry['movies']
        result_message_id = db_entry['message_id']
            
        await query.answer()
        await send_result_message(client, query.message, query_text, movies, int(page), result_message_id)
    else:
        await query.answer("Thats not for you!!", show_alert=True)
    
@Client.on_callback_query(filters.regex(r'^previous_page:'))
async def previous_page_callback(client: Client, query: CallbackQuery):
    data = query.data
    _, query_text, page = data.split(':')
        
    # Retrieve data from DATABASE
    db_entry = DATABASE.get(query_text)
    if db_entry:
        movies = db_entry['movies']
        result_message_id = db_entry['message_id']
            
        await query.answer()
        await send_result_message(client, query.message, query_text, movies, int(page), result_message_id)
    else:
        await query.answer("Thats not for you!!", show_alert=True)
