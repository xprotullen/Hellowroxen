# (c) @TheLx0980
# Year: 2023 

from . import Database
db = Database()


def add_channel(group_id, channel_id):
    query = {"group_id": group_id}
    update = {"$set": {"channel_id": channel_id}}
    collection.update_one(query, update, upsert=True)


def is_group_in_database(group_id):
    query = {"group_id": group_id}
    result = collection.find_one(query)
    return result is not None

def get_channel_id(group_id):
    query = {"group_id": group_id}
    result = collection.find_one(query)
    return result["channel_id"] if result else None

def delete_channel(group_id):
    query = {"group_id": group_id}
    collection.delete_one(query)
