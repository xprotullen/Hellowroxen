# (c) @TheLx0980

from . import Database

db = Database()

class AuthorizedChannels:
    authorized_channels = db.authorized_channels
    
    @staticmethod
    def get_authorized_channels(channel_id):
        channels = AuthorizedChannels.authorized_channels.find({"channel_id": channel_id})
        return [channel["channel_id"] for channel in channels]
    
    @staticmethod
    def delete_authorized_channel(channel_id):
        AuthorizedChannels.authorized_channels.delete_one({"channel_id": channel_id})
    
    @staticmethod
    def add_authorized_channel(channel_id):
        AuthorizedChannels.authorized_channels.insert_one({"channel_id": channel_id})
    
    @staticmethod
    def delete_all_authorized_chats():
        result = AuthorizedChannels.authorized_channels.delete_many({})
        return result.deleted_count
    
    @staticmethod
    def get_authorized_chat():
        channels = AuthorizedChannels.authorized_channels.find({})
        return [channel["channel_id"] for channel in channels]


    
    
