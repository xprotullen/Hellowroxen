# @thelx0980

from pymongo import MongoClient
from wroxen.vars import DB_URL

# Set up MongoDB connection
client = MongoClient(DB_URL)
db = client["bot_caption_database"]
channels_collection = db["channels"]

def add_channel(channel_id, caption):
    channel_data = {"channel_id": channel_id, "caption": caption}
    channels_collection.insert_one(channel_data)

def delete_channel(channel_id):
    channels_collection.delete_one({"channel_id": channel_id})

def get_caption(channel_id):
    channel_data = channels_collection.find_one({"channel_id": channel_id})
    if channel_data:
        return channel_data["caption"]
    return None
