# (c) TheLx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, enums
from wroxen.wroxen import Wroxen
from wroxen.text import ChatMSG
import logging

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


@Client.on_callback_query()
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


    elif query_data == "close":
        await update.message.delete()
