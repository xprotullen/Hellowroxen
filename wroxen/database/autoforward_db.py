# (c) @TheLx0980

from wroxen.database import db


forward_collection = db["forward_settings"]

def set_forward_settings(from_chat, to_chat):
    forward_data = {"from_chat": int(from_chat), "to_chat": int(to_chat)}
    forward_collection.insert_one(forward_data)

def get_forward_settings():
    return forward_collection.find_one()
