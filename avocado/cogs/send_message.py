import discord
from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def send_to(self, ctx, mention: discord.TextChannel, *args):
        message = "\n".join(args)
        await mention.send(message)