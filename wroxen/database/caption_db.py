# @thelx0980

from pymongo import MongoClient
from wroxen.vars import DB_URL

# Set up MongoDB connection
client = MongoClient(DB_URL)
db = client["bot_caption_database"]
channels_collection = db["channels"]
forward_collection = db["forward_settings"]
replace_collection = db["replace_settings"]

def add_channel(channel_id, caption):
    existing_channel = channels_collection.find_one({"channel_id": channel_id})
    if existing_channel:
        raise ValueError("Your channel is already available in the database.")

    channel_data = {"channel_id": channel_id, "caption": caption}
    channels_collection.insert_one(channel_data)


def delete_channel(channel_id):
    channels_collection.delete_one({"channel_id": channel_id})

def get_caption(channel_id):
    channel_data = channels_collection.find_one({"channel_id": channel_id})
    if channel_data:
        return channel_data["caption"]
    return None

def update_caption(channel_id, new_caption):
    channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"caption": new_caption}}
    )
    
def is_channel_added(channel_id):
    channel_doc = channels_collection.find_one({"channel_id": channel_id})
    return channel_doc is not None

#______________________________________________________________________________#

def set_forward_settings(from_chat, to_chat):
    existing_settings = forward_collection.find_one({"from_chat": from_chat})

    if existing_settings:
        raise ValueError("Forwarding settings are already added.")

    forward_data = {"from_chat": from_chat, "to_chat": to_chat}
    forward_collection.insert_one(forward_data)

def get_forward_settings(channel_id):
    forward_settings = forward_collection.find_one(
        {"$or": [{"from_chat": channel_id}, {"to_chat": channel_id}]}
    )

    replace_settings = replace_collection.find_one({"channel_id": channel_id})

    if forward_settings and replace_settings:
        forward_settings["replace_text"] = {
            "old_username": replace_settings.get("old_username"),
            "new_username": replace_settings.get("new_username")
        }
        forward_settings["caption"] = replace_settings.get("caption")

    return forward_settings

def add_forward_settings(from_chat, to_chat):
    forward_settings = {
        "from_chat": from_chat,
        "to_chat": to_chat
    }
    forward_collection.insert_one(forward_settings)

def add_replace_settings(channel_id, old_username, new_username):
    replace_settings = {
        "channel_id": channel_id,
        "old_username": old_username,
        "new_username": new_username
    }
    replace_collection.insert_one(replace_settings)

def add_caption(channel_id, caption):
    replace_settings = replace_collection.find_one({"channel_id": channel_id})
    if replace_settings:
        replace_settings["caption"] = caption
        replace_collection.update_one(
            {"channel_id": channel_id},
            {"$set": replace_settings},
            upsert=True
        )
    else:
        replace_settings = {
            "channel_id": channel_id,
            "caption": caption
        }
        replace_collection.insert_one(replace_settings)

def delete_caption_settings(channel_id):
    replace_collection.update_one(
        {"channel_id": channel_id},
        {"$unset": {"caption": ""}}
    )


def delete_caption_settings(channel_id):
    replace_collection.delete_one({"channel_id": channel_id})

    
    
def delete_forward_settings(channel_id):
    delete_result = forward_collection.delete_many({
        "$or": [
            {"from_chat": channel_id},
            {"to_chat": channel_id}
        ]
    })
    return delete_result.deleted_count

def delete_replace_settings(channel_id):
    replace_collection.delete_one({"channel_id": channel_id})

def update_forward_settings(channel_id, forward_settings):
    forward_collection.update_one(
        {"$or": [{"from_chat": channel_id}, {"to_chat": channel_id}]},
        {"$set": forward_settings},
        upsert=True
    )



    
def clear_forward_db():
    delete_result = forward_collection.delete_many({})
    return delete_result.deleted_count
