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
    #print("Deleted Message: ", message.content)
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
    channel = client.get_channel(int(CHANNEL_ACTIVE_DEVELOPING))
    if channel:
        await channel.send("Byte is online, and always watching...")

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
    channel_handlers = {
        CHANNEL_ACTIVE_DEVELOPING: on_message_active_developing,
        CHANNEL_GENERAL: on_message_general
    }

    for channel_id, handler in channel_handlers.items():
        if message.channel.id == channel_id:
            await handler(message)
            break

async def on_message_active_developing(message):
    await channel_log_active_developing(message)

async def on_message_general(message):
    await channel_log_general(message)


logging_functions = {
    CHANNEL_GENERAL: deleted_messages_general,
    CHANNEL_ACTIVE_DEVELOPING: deleted_messages_active_developing
}

@client.event
async def on_message_delete(message):
    channel_id = message.channel.id
    logging_function = logging_functions.get(channel_id)
    if logging_function:
        print(f"{channel_id}: {message.content}")
        await logging_function(message)


client.run(TOKEN)

