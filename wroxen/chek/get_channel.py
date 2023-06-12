# (c) @TheLx0980

from wroxen.database import Database 
db = Database ()

def get_channel_info(user_id):
    channel_doc = db.channels_collection.find_one({"user_id": user_id})
    if channel_doc:
        channel_id = channel_doc["channel_id"]
        caption = db.get_caption(user_id, channel_id)
        return channel_id, caption
    return None, None

def is_channel_added(channel_id):
    channel_doc = db.channels_collection.find_one({"channel_id": channel_id})
    return channel_doc is not None
