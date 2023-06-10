# (c) @TheLx0980

from . import authorized_channels

def get_authorized_channels():
    """
    Retrieve all authorized channels from the MongoDB database.
    """
    channels = authorized_channels.find()
    return [channel["channel_id"] for channel in channels]
