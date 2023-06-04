# @thelx0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters, enums
from wroxen import Wroxen
from wroxen.text import ChatMSG

@Wroxen.on_callback_query()
async def callback_data(bot, update: CallbackQuery):

    query_data = update.data

    if query_data == "start":
        buttons = [[            
            InlineKeyboardButton('Help ⚙', callback_data="help")
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
            InlineKeyboardButton('Home ⚡', callback_data='start'),
            InlineKeyboardButton('About', callback_data='about')
        ],[
            InlineKeyboardButton('Close 🔐', callback_data='close')
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
            InlineKeyboardButton('Home ⚡', callback_data='start'),
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            ChatMSG.ABOUT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif query_data == "close":
        await update.message.delete()