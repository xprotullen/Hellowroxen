# @thelx0980

from pymongo import MongoClient
from wroxen.vars import DB_URL


class Database:
    def __init__(self):
        self.client = MongoClient(DB_URL)
        self.db = self.client["bot_caption_database"]
        self.channels_collection = self.db["channels"]
        self.forward_collection = self.db["forward_settings"]
        self.caption_collection = self.db["caption_settings"]
        self.authorized_channels = self.db["authorized_channel"]
        self.user_collection = self.db["user-collection"]
    
    def add_user(self, user_id):
        existing_user = self.user_collection.find_one({"user_id": user_id})
        if not existing_user:
            user_data = {"user_id": user_id}        
            self.user_collection.insert_one(user_data)

    
    def get_user(self, user_id):
        existing_user = self.user_collection.find_one({"user_id": user_id})
        if existing_user:
            return existing_user['user_id']
        return None
        
    
    def add_channel(self, channel_id, caption):
        existing_channel = self.channels_collection.find_one({"channel_id": channel_id})
        if existing_channel:
            raise ValueError("Your channel is already available in the database.")

        channel_data = {"channel_id": channel_id, "caption": caption}
        self.channels_collection.insert_one(channel_data)

    def delete_channel(self, channel_id):
        self.channels_collection.delete_one({"channel_id": channel_id})

    def get_caption(self, channel_id):
        channel_data = self.channels_collection.find_one({"channel_id": channel_id})
        if channel_data:
            return channel_data["caption"]
        return None

    def update_caption(self, channel_id, new_caption):
        self.channels_collection.update_one(
            {"channel_id": channel_id},
            {"$set": {"caption": new_caption}}
        )

    def is_channel_added(self, channel_id):
        channel_doc = self.channels_collection.find_one({"channel_id": channel_id})
        return channel_doc is not None

    def set_forward_settings(self, from_chat, to_chat):
        existing_settings = self.forward_collection.find_one({"from_chat": from_chat})

        if existing_settings:
            raise ValueError("Forwarding settings are already added.")

        forward_data = {"from_chat": from_chat, "to_chat": to_chat}
        self.forward_collection.insert_one(forward_data)

    def get_forward_settings(self, channel_id):
        forward_settings = self.forward_collection.find_one(
            {"$or": [{"from_chat": channel_id}, {"to_chat": channel_id}]}
        )

        return forward_settings

    def add_forward_settings(self, from_chat, to_chat):
        forward_settings = {
            "from_chat": from_chat,
            "to_chat": to_chat
        }
        self.forward_collection.insert_one(forward_settings)

    def delete_forward_settings(self, channel_id):
        delete_result = self.forward_collection.delete_many({
            "$or": [
                {"from_chat": channel_id},
                {"to_chat": channel_id}
            ]
        })
        return delete_result.deleted_count

    def update_f_caption(self, channel_id, new_caption):
        replace_settings = self.caption_collection.find_one({"channel_id": channel_id})
        if replace_settings:
            replace_settings["caption"] = new_caption
            self.caption_collection.update_one(
                {"channel_id": channel_id},
                {"$set": replace_settings},
                upsert=True
            )
            return True
        return False
    
    def update_replace_text (self, channel_id, old_username, new_username):
        replace_settings = self.caption_collection.find_one({"channel_id": channel_id})
        if replace_settings:
            replace_settings["old_username"] = old_username
            replace_settings["new_username"] = new_username
            self.caption_collection.update_one(
                {"channel_id": channel_id},
                {"$set": replace_settings}
            )
            return True
        return False

    def add_replace_settings(self, channel_id, old_username, new_username, caption):
        existing_settings = self.caption_collection.find_one({"channel_id": channel_id})
        if existing_settings:
            raise ValueError("Replace settings for this channel already exist.")

        replace_settings = {
            "channel_id": channel_id,
            "old_username": old_username,
            "new_username": new_username,
            "caption": caption
        }
        self.caption_collection.insert_one(replace_settings)

    def delete_caption_settings(self, channel_id):
        existing_settings = self.caption_collection.find_one({"channel_id": channel_id})
        if existing_settings:
            existing_settings["caption"] = ""
            self.caption_collection.update_one(
                {"channel_id": channel_id},
                {"$set": existing_settings}
            )
        else:
            raise ValueError("Replace settings for this channel do not exist.")

    def delete_replace_settings(self, channel_id, old_username, new_username):
        existing_settings = self.caption_collection.find_one({"channel_id": channel_id})
        if existing_settings:
            existing_settings["old_username"] = ""
            existing_settings["new_username"] = ""
            self.caption_collection.update_one(
                {"channel_id": channel_id},
                {"$set": existing_settings}
            )
        else:
            raise ValueError("Replace settings for this channel do not exist.")

    def get_replace_data(self, channel_id):
        replace_data = self.caption_collection.find_one({"channel_id": channel_id})
        if replace_data:
            old_username = replace_data["old_username"]
            new_username = replace_data["new_username"]
            caption = replace_data["caption"]
            return old_username, new_username, caption
        else:
            return None, None, None

    def clear_forward_db(self):
        delete_result = self.forward_collection.delete_many({})
        return delete_result.deleted_count

    def clear_all_db(self):
        ab = self.forward_collection.delete_many({}).deleted_count
        cd = self.authorized_channels.delete_many({}).deleted_count
        ef = self.caption_collection.delete_many({}).deleted_count
        gh = self.channels_collection.delete_many({}).deleted_count

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

    


