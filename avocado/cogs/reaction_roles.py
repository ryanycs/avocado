import discord
from discord.ext import commands


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = 1229718858152153099  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 1229697235646943286,  # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='🟠'): 1229697442161623111,  # ID of the role associated with unicode emoji '🟠'.
            discord.PartialEmoji(name='🟡'): 1229697600563843144,  # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='🟢'): 1229697686442082354,  # ID of the role associated with unicode emoji '🟢'.
            discord.PartialEmoji(name='🔵'): 1229698118950453289,  # ID of the role associated with unicode emoji '🔵'.
            discord.PartialEmoji(name='🟣'): 1229697876007845889,  # ID of the role associated with unicode emoji '🟣'.
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return
        
        # remove other reactions if the user has reacted to a different emoji
        message = await self.bot.get_channel(payload.channel_id).fetch_message(self.role_message_id)
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.id == payload.user_id and str(reaction.emoji) != str(payload.emoji):
                    await message.remove_reaction(reaction.emoji, user)
                    break

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return
        
        if payload.member == self.bot.user:
            # Make sure the bot doesn't assign the role to itself.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None or member == self.bot.user:
            # Make sure the member still exists and is valid.
            # and that the bot doesn't remove the role from itself.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
