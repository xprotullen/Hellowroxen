# (c) @TheLx0980
# Year: 2023 

from . import Database

Db = Database()
DB = Db.db
auto_search_db = DB["auto_search_collection"]


def add_channel(group_id, channel_id):
    query = {"group_id": group_id}
    update = {"$set": {"channel_id": channel_id}}
    auto_search_db.update_one(query, update, upsert=True)


def is_group_in_database(group_id):
    query = {"group_id": group_id}
    result = auto_search_db.find_one(query)
    return result is not None

def get_channel_id(group_id):
    query = {"group_id": group_id}
    result = auto_search_db.find_one(query)
    return result["channel_id"] if result else None

def delete_channel(group_id):
    query = {"group_id": group_id}
    auto_search_db.delete_one(query)
