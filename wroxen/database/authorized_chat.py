# (c) @TheLx0980

from . import Database

db = Database()
Auth = db.authorized_channels

class AuthorizedChannels:
    @staticmethod
    def get_authorized_channels(channel_id):
        channels = Auth.find({"channel_id": channel_id})
        return [channel["channel_id"] for channel in channels]
    
    @staticmethod  
    def delete_authorized_channel(channel_id):
        Auth.delete_one({"channel_id": channel_id})
    
    @staticmethod
    def add_authorized_channel(channel_id):
        Auth.insert_one({"channel_id": channel_id})
    
    @staticmethod
    def delete_all_authorized_chats():
        result = Auth.delete_many({})
        return result.deleted_count
    
    @staticmethod
    def get_authorized_chat():
        channels = Auth.find({})
        return [channel["channel_id"] for channel in channels]


    
    
