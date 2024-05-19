import os
import discord
import json
import loggingmessages
from loggingmessages import log_channel_message
from discord.ext import commands
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




@client.event
async def on_message(message):
    if message.author == client.user:
        return

    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
  
    message_data = {
        "message_id": message.id,
        "content": message.content,
        "channel": {
            "id": message.channel.id
        },
        "author": {
            "name": message.author.name,
            "nick": message.author.nick,
            "id": message.author.id
        },
        "guild": {
            "name": message.guild.name,
            "id": message.guild.id
        },
        "timestamp": timestamp
    }
   
    message_json = json.dumps(message_data, indent=4)

    log_message(message.channel.name, message_json)




@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
  
    message_data = {
        "message_id": message.id,
        "content": message.content,
        "channel": {
            "id": message.channel.id
        },
        "author": {
            "name": message.author.name,
            "nick": message.author.nick,
            "id": message.author.id
        },
        "guild": {
            "name": message.guild.name,
            "id": message.guild.id
        },
        "timestamp": timestamp
    }
   
    message_json = json.dumps(message_data, indent=4)

    log_message_deleted(message.channel.name, message_json)





def log_message(channel_name, message_json):
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_path = os.path.join(log_dir, f"{channel_name}.json")

    
    with open(file_path, "a") as log_file:
        log_file.write(message_json + "\n")




def log_message_deleted(channel_name, message_json):
    
    log_dir = "logsdeleted"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_path = os.path.join(log_dir, f"{channel_name}.json")

    
    with open(file_path, "a") as log_file:
        log_file.write(message_json + "\n")




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

# @client.event
# async def on_disconnect():
#     for channel_id in send_messages_to:
#         channel = client.get_channel(int(channel_id))
#         if channel:
#             await channel.send("Byte is offline...")


client.run(token)
