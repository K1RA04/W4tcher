import json
import discord
import os
from discord.ext import commands

def log_channel_message(channel_id, message):
    channel_UID = channel_id
    log_file_path = f"Logs/channel_{channel_UID}/channel-log-{channel_UID}.json"

    author = message.author

    data = {
        "author": {
            "id": str(author.id),
            "name": author.name,
            "discriminator": author.discriminator,
        },
        "content": message.content,
        "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "channel": {
            "id": str(channel_id),
            "name": channel_name
        }
    }

    with open(log_file_path, "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write('\n')
