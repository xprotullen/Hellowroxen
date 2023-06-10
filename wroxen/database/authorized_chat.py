# (c) @TheLx0980

from . import authorized_channels

def get_authorized_channels():
    channels = authorized_channels.find()
    return [channel["channel_id"] for channel in channels]

def delete_authorized_channel(channel_id):
    authorized_channels.delete_one({"channel_id": channel_id})

def add_authorized_channel(channel_id):
    authorized_channels.insert_one({"channel_id": channel_id})
    
def delete_all_authorized_chats()
    authorized_channels.delete_many({})

    
    
    
    
    
