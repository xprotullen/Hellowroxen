# @thelx0980

from pymongo import MongoClient
from wroxen.vars import DB_URL

# Set up MongoDB connection
client = MongoClient(DB_URL)
db = client["bot_caption_database"]
channels_collection = db["channels"]
forward_collection = db["forward_settings"]
caption_collection = db["caption_settings"]
authorized_channels = db["authorized_channel"]

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

    return forward_settings


def add_forward_settings(from_chat, to_chat):
    forward_settings = {
        "from_chat": from_chat,
        "to_chat": to_chat
    }
    forward_collection.insert_one(forward_settings)

    
def delete_forward_settings(channel_id):
    delete_result = forward_collection.delete_many({
        "$or": [
            {"from_chat": channel_id},
            {"to_chat": channel_id}
        ]
    })
    return delete_result.deleted_count

#'__&
def update_f_caption(channel_id, new_caption):
    replace_settings = caption_collection.find_one({"channel_id": channel_id})
    if replace_settings:
        replace_settings["caption"] = new_caption
        caption_collection.update_one(
            {"channel_id": channel_id},
            {"$set": replace_settings},
            upsert=True
        )
        return True
    return False


def update_replace_text(channel_id, old_username, new_username):
    replace_settings = caption_collection.find_one({"channel_id": channel_id})
    if replace_settings:
        replace_settings["old_username"] = old_username
        replace_settings["new_username"] = new_username
        caption_collection.update_one(
            {"channel_id": channel_id},
            {"$set": replace_settings},
        )
        return True
    return False


def add_replace_settings(channel_id, old_username, new_username, caption):
    existing_settings = caption_collection.find_one({"channel_id": channel_id})
    if existing_settings:
        raise ValueError("Replace settings for this channel already exist.")

    replace_settings = {
        "channel_id": channel_id,
        "old_username": old_username,
        "new_username": new_username,
        "caption": caption
    }
    caption_collection.insert_one(replace_settings)



def delete_caption_settings(channel_id):
    existing_settings = caption_collection.find_one({"channel_id": channel_id})
    if existing_settings:
        existing_settings["caption"] = ""
        caption_collection.update_one(
            {"channel_id": channel_id},
            {"$set": existing_settings}
        )
    else:
        raise ValueError("Replace settings for this channel do not exist.")
    
    
def delete_replace_settings(channel_id, old_username, new_username):
    existing_settings = caption_collection.find_one({"channel_id": channel_id})
    if existing_settings:
        existing_settings["old_username"] = ""
        existing_settings["new_username"] = ""
        caption_collection.update_one(
            {"channel_id": channel_id},
            {"$set": existing_settings}
        )
    else:
        raise ValueError("Replace settings for this channel do not exist.")

def get_replace_data(channel_id):
    replace_data = caption_collection.find_one({"channel_id": channel_id})
    if replace_data:
        old_username = replace_data["old_username"]
        new_username = replace_data["new_username"]
        caption = replace_data["caption"]
        return old_username, new_username, caption
    else:
        return None, None, None


def clear_forward_db():
    delete_result = forward_collection.delete_many({})
    return delete_result.deleted_count

# पूरे डेटाबेस को हटा दें।
def clear_all_db():
    ab = forward_collection.delete_many({}).deleted_count
    cd = authorized_channels.delete_many({}).deleted_count
    ef = caption_collection.delete_many({}).deleted_count
    gh = channels_collection.delete_many({}).deleted_count

    total_count = (
        ab +
        cd +
        ef +
        gh
    )
    return {
        'a1': ab,
        'a2': cd,
        'a3': ef,
        'a4': gh,
        'a5': total_count
    }

