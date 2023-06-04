


@Client.on_message(filters.command("set_caption"))
async def set_caption_command(bot, message):
    user_id = message.from_user.id
    command_parts = message.text.split(" ", 3)

    if len(command_parts) < 4:
        await message.reply("Please provide both the channel ID and the caption.")
        return

    channel_id = command_parts[1]
    caption = command_parts[2]

    set_caption(user_id, channel_id, caption)
    await message.reply(f"Caption set for channel {channel_id}.")

    
 @Client.on_message(filters.command("delete_info"))
async def delete_info_command(bot, message):
    user_id = message.from_user.id
    command_parts = message.text.split(" ", 2)

    if len(command_parts) < 2:
        await message.reply("Please provide the channel ID to delete.")
        return

    channel_id = command_parts[1]

    delete_info(user_id, channel_id)
    await message.reply(f"Channel ID and caption deleted for channel {channel_id}.")


@Client.on_message(filters.command("delete_caption"))
async def delete_caption_command(bot, message):
    user_id = message.from_user.id
    command_parts = message.text.split(" ", 2)

    if len(command_parts) < 2:
        await message.reply("Please provide the channel ID to delete the caption.")
        return

    channel_id = command_parts[1]

    deleted = delete_caption(user_id, channel_id)
    if deleted:
        await message.reply(f"Caption deleted for channel {channel_id}.")
    else:
        await message.reply("No caption found for the specified channel.")

def delete_caption(user_id, channel_id):
    result = captions_collection.delete_one({"user_id": user_id, "channel_id": channel_id})
    return result.deleted_count > 0
  
