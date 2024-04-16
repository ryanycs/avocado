import os

import discord
from discord.ext import commands

from .cogs import Message, ReactionRoles


class Avocado(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        await bot.add_cog(ReactionRoles(bot))
        await bot.add_cog(Message(bot))
        print(f"We have logged in as {self.user}")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Avocado(command_prefix="/", intents=intents)