# (c) @TheLx0980

from wroxen.database import db as DB

group_search_collection = DB["group_search"]

def add_group_search(group_id, search_channel_id):
    group_search_data = {"group_id": group_id, "search_channel_id": search_channel_id}
    group_search_collection.insert_one(group_search_data)

def get_search_channel_id(group_id):
    group_search_data = group_search_collection.find_one({"group_id": group_id})
    if group_search_data:
        return group_search_data["search_channel_id"]
    return None
  
 def update_group_search(group_id, search_channel_id):
    group_search_collection.update_one(
        {"group_id": group_id},
        {"$set": {"search_channel_id": search_channel_id}}
    ) 
  
def delete_group_search(group_id):
    group_search_collection.delete_one({"group_id": group_id}) 
  
  
  
