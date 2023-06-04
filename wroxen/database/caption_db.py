# @thelx0980

from pymongo import MongoClient
from wroxen import DB_URL

# Set up MongoDB connection 
client = MongoClient(DB_URL)
db = client["bot_caption_database"]
channels_collection = db["channels"]
captions_collection = db["captions"]

def set_caption(user_id, channel_id, caption):
    captions_collection.update_one({"user_id": user_id, "channel_id": channel_id}, {"$set": {"caption": caption}}, upsert=True)

def delete_caption(user_id, channel_id):
    captions_collection.delete_one({"user_id": user_id, "channel_id": channel_id})

def get_caption(user_id, channel_id):
    caption_doc = captions_collection.find_one({"user_id": user_id, "channel_id": channel_id})
    if caption_doc:
        return caption_doc["caption"]
    return None
