# (c) TheLx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, enums
from wroxen.wroxen import Wroxen
from wroxen.text import ChatMSG
from wroxen.vars import ADMIN_IDS
from .search_msg import DATABASE 

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Wroxen.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    await message.reply(
        text=ChatMSG.START_TXT.format(message.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("मदद ⚙", callback_data = "help"),
                    InlineKeyboardButton("🔒 बंद करो", callback_data = "close")
                ]
            ]
        ),
        quote=True
    )
    

@Wroxen.on_message(filters.command("help") & filters.private & filters.incoming)
async def about(client, message):
    await message.reply(
        text=ChatMSG.HELP_TXT,
        disable_web_page_preview=True,
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 मेरे बारे में", callback_data = "about"),
                    InlineKeyboardButton("🔒 बंद करो", callback_data = "close")
                ]
            ]
        ),
        quote=True
    )


HELLO = """ @Client.on_callback_query()
async def callback_data(bot, update: CallbackQuery):

    query_data = update.data

    if query_data == "start":
        buttons = [[            
            InlineKeyboardButton('मदद ⚙', callback_data="help"),
            InlineKeyboardButton("🔒 बंद करो", callback_data = "close")
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.START_TXT.format(update.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )


    elif query_data == "help":
        buttons = [[
            InlineKeyboardButton('पीछे जाए ⚡', callback_data='start'),
            InlineKeyboardButton('मेरे बारे में', callback_data='about')
        ],[
            InlineKeyboardButton('स्वचालित कैप्शन', callback_data='caption')
        ],[
            InlineKeyboardButton('स्वचालित फ़ॉरवर्ड', callback_data='autoforward')
        ],[
            InlineKeyboardButton('मीडिया क्लोन', callback_data='media_clone')
        ],[
            InlineKeyboardButton('व्यवस्थापक आदेश', callback_data='admin_command')
        ],[ 
            InlineKeyboardButton('चैनल में खोजें', callback_data='channel_search')
        ],[
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.HELP_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )


    elif query_data == "about": 
        buttons = [[
            InlineKeyboardButton('पीछे ⚡', callback_data='start'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.ABOUT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query_data == "caption": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.CAPTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
  
    elif query_data == "autoforward": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.AUTO_FORWARD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query_data == "admin_command": 
        user_id = update.from_user.id
        if user_id not in ADMIN_IDS:            
            await update.answer("आप बोट व्यवस्थापक नहीं है।",show_alert=True)
            return
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.ADMIN_COMMAND_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query_data == "media_clone": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.MEDIA_CLONE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query_data == "channel_search": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.CHANNEL_SEARCH_TXT,  
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
    )


    elif query_data == "close":
        await update.message.delete()
"""

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
            await query.answer("Thats not for you!!", show_alert=True)
    
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
            await query.answer("Thats not for you!!", show_alert=True)
    
    elif data == "start":
        buttons = [[            
            InlineKeyboardButton('मदद ⚙', callback_data="help"),
            InlineKeyboardButton("🔒 बंद करो", callback_data="close")
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.START_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    elif data == "help":
        buttons = [[
            InlineKeyboardButton('पीछे जाए ⚡', callback_data='start'),
            InlineKeyboardButton('मेरे बारे में', callback_data='about')
        ], [
            InlineKeyboardButton('स्वचालित कैप्शन', callback_data='caption')
        ], [
            InlineKeyboardButton('स्वचालित फ़ॉरवर्ड', callback_data='autoforward')
        ], [
            InlineKeyboardButton('मीडिया क्लोन', callback_data='media_clone')
        ], [
            InlineKeyboardButton('व्यवस्थापक आदेश', callback_data='admin_command')
        ], [ 
            InlineKeyboardButton('चैनल में खोजें', callback_data='channel_search')
        ], [
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.HELP_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    elif data == "about": 
        buttons = [[
            InlineKeyboardButton('पीछे ⚡', callback_data='start'),
                        InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.ABOUT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif data == "caption": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.CAPTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
  
    elif data == "autoforward": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.AUTO_FORWARD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif data == "admin_command": 
        user_id = query.from_user.id
        if user_id not in ADMIN_IDS:            
            await query.answer("आप बोट व्यवस्थापक नहीं है।", show_alert=True)
            return
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.ADMIN_COMMAND_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif data == "media_clone": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.MEDIA_CLONE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "channel_search": 
        buttons = [[
            InlineKeyboardButton('पीछे⚡', callback_data='help'),
            InlineKeyboardButton('बंद करें 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            ChatMSG.CHANNEL_SEARCH_TXT,  
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "close":
        await query.message.delete()



