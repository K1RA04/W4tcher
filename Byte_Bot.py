import os
import discord
import json
from discord.ext import commands
from Functions import commands

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')
user_id = os.getenv('USER_ID')
active_developing = int(os.getenv('CHANNEL_ACTIVE_DEVELOPING'))
general= int(os.getenv('CHANNEL_GENERAL'))
all_in  = int(os.getenv('CHANNEL_ALL_IN'))
chit_chat = int(os.getenv('VOICE_CHANNEL_CHIT_CHAT'))
send_messages_to = [os.getenv('CHANNEL_ACTIVE_DEVELOPING'), os.getenv('CHANNEL_ALL_IN')]

intents = discord.Intents.all()

client = discord.Client(intents=intents)

nonos = ["hs", "!leaderboard"]


# @client.event
# async def on_voice_state_connect(member, before, after):
#     if after.channel and after.channel.id == chit_chat:
#         user = member.display_name
#         await member.guild.owner.send(f"{user} has joined {after.channel.name}.")

async def slur_context(message):
    author = message.author
    content = message.content
    channel = message.channel
    
    report = f"**Byte-Report**\n" \
             f"Author: {author.name}#{author.discriminator}\n" \
             f"Content: {content}\n" \
             f"Channel: {channel.name} (ID: {channel.id})\n" \

    user = await client.fetch_user(user_id)
    await user.send(report)


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
    for channel_id in send_messages_to:
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.send("Byte is online, and always watching...")

    for guild in client.guilds:
        if guild.name == guild:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    session_id = client.ws.session_id

    await write_session_info(guild, session_id)

@client.event
async def on_disconnect():
    for channel_id in send_messages_to:
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.send("Byte is offline...")

@client.event
async def on_message(message):
    channel_handlers = {
        active_developing: on_message_active_developing,
        general: on_message_general
    }

    for channel_id, handler in channel_handlers.items():
        if message.channel.id == channel_id:
            await handler(message)
            break

    if message.author == client.user: 
        return

    for slur in nonos:
        if slur in message.content.lower():
            await slur_context(message)
            break 

async def on_message_active_developing(message):
    await channel_log_active_developing(message)

async def on_message_general(message):
    await channel_log_general(message)


logging_functions = {
    general: deleted_messages_general,
    active_developing: deleted_messages_active_developing
}

@client.event
async def on_message_delete(message):
    channel_id = message.channel.id
    logging_function = logging_functions.get(channel_id)
    if logging_function:
        print(f"{channel_id}: {message.content}")
        await logging_function(message)


client.run(token)

