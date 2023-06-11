# @thelx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters, enums
from wroxen.wroxen import Wroxen
from wroxen.text import ChatMSG
From .Clone.py import FORWARDING

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)



@Client.on_callback_query(filters.regex(r'^callback_data_regex'))
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

        
@Client.on_callback_query(filters.regex(r'^forward'))
async def forward(bot, query):
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
