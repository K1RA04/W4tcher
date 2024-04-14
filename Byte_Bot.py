import os
import discord
import json
from discord.ext import commands
from Functions import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ACTIVE_DEVELOPING = int(os.getenv('CHANNEL_ACTIVE_DEVELOPING'))
CHANNEL_GENERAL= int(os.getenv('CHANNEL_GENERAL'))

intents = discord.Intents.all()




client = discord.Client(intents=intents)

async def channel_log_active_developing(message):
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
            "id": str(message.channel.id),
            "name": message.channel.name
        }
    }

    with open("Logs\channel_active_developing\channel-log-activedeveloping.json", "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write('\n')

async def deleted_messages_active_developing(message):
    print("Deleted Message: ", message.content)
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
            "id": str(message.channel.id),
            "name": message.channel.name
        }
    }

    file_path = "Logs/channel_active_developing/deleted-messages-log.json"
    print("File path:", file_path)

    with open(file_path, "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write('\n')


async def channel_log_general(message):
    author = message.author

    data = {
        "author": {
            "id": str(author.id),
            "name": author.name,
            "discriminator": author.discriminator,
            "avatar_url": str(author.avatar_url) if hasattr(author, 'avatar_url') else None
        },
        "content": message.content,
        "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "channel": {
            "id": str(message.channel.id),
            "name": message.channel.name
        }
    }

    with open("Logs\channel_general\channel-log-general.json", "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write('\n')

async def deleted_messages_general(message):
    print("Deleted Message: ", message.content)
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
            "id": str(message.channel.id),
            "name": message.channel.name
        }
    }

    file_path = "Logs/channel_general/deleted-messages-log.json"
    print("File path:", file_path)

    with open(file_path, "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write('\n')

async def write_session_info(guild, session_id):
    data = {
        "guild": {
            "id": str(guild.id),
            "name": guild.name
        },
        "session": {
            "id": session_id
        }
    }

    with open("sessioninfo.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    session_id = client.ws.session_id

    await write_session_info(guild, session_id)

@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ACTIVE_DEVELOPING:
        await on_message_active_developing(message)
    elif message.channel.id == CHANNEL_GENERAL:
        await on_message_general(message)

async def on_message_active_developing(message):
    await channel_log_active_developing(message)

async def on_message_general(message):
    await channel_log_general(message)

client.run(TOKEN)
