# (c) @TheLx0980

from . import authorized_channels

def get_authorized_channels(channel_id):
    channels = authorized_channels.find({"channel_id": channel_id})
    return [channel["channel_id"] for channel in channels]

def delete_authorized_channel(channel_id):
    authorized_channels.delete_one({"channel_id": channel_id})

def add_authorized_channel(channel_id):
    authorized_channels.insert_one({"channel_id": channel_id})
    
def delete_all_authorized_chats():
    result = authorized_channels.delete_many({})
    return result.deleted_count

    
def get_authorized_chat():
    channels = authorized_channels.find({})
    return [channel["channel_id"] for channel in channels]

    
    
