# @thelx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters, enums
from wroxen.wroxen import Wroxen
from wroxen.text import ChatMSG

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)



@Client.on_callback_query()
async def callback_data(bot, update: CallbackQuery):

    query_data = update.data

    if query_data == "start":
        buttons = [[            
            InlineKeyboardButton('मदद ⚙', callback_data="help")
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
            #InlineKeyboardButton('About', callback_data='about')
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


    elif query_data == "close":
        await update.message.delete()

        
