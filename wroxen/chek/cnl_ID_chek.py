# (c) TheLx0980
"""
import pyrogram


async def is_valid_channel_id(channel_id):
    try:
        chat = await bot.get_chat(channel_id)
        if chat.type == pyrogram.enums.ChatType.CHANNEL:  
            return True
        else:
            return False
    except pyrogram.errors.FloodWait as e:       
        print(f"FloodWait error: {e}")
        return False
    except pyrogram.errors.ChatAdminRequired as e:
        print(f"ChatAdminRequired error: {e}")
        return False
    except pyrogram.errors.ChannelInvalid as e:               
        print(f"ChannelInvalid error: {e}")
        return False
""'
