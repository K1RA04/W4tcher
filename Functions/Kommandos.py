# from discord.ext import commands

# class CustomCommands(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command(name='get_channel_ids')
#     async def get_channel_ids(self, ctx):
#         guild = ctx.guild
#         channel_ids = [channel.id for channel in guild.channels]
#         channel_ids_str = '\n'.join(str(id) for id in channel_ids)
        
#         with open(".env", "a") as env_file:
#             env_file.write("\n# Channel IDs\n")
#             env_file.write("CHANNEL_IDS=\n")
#             env_file.write(channel_ids_str)

#         await ctx.send("Channel IDs wurden erfolgreich in die .env Datei geschrieben.")

# def setup(bot):
#     bot.add_cog(CustomCommands(bot))