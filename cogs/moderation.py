import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Purge messages command
    @app_commands.command(description="Clear the messages")
    @app_commands.describe(limit="number of messages")
    @app_commands.describe(reason="Reason for the purge")
    @app_commands.checks.has_permissions(ban_members=True)
    async def purge(self, interaction: discord.Interaction, limit: int, reason: str):

        await interaction.response.defer(ephemeral=True)
        try:
            deleted = await interaction.channel.purge(limit=limit, reason=reason)
            await interaction.followup.send(
                f"Deleted {len(deleted)} message(s) for the reason: {reason}"
            )
        except Exception as e:
            await interaction.followup.send(f"an error was found {e}")

    # Ban member command
    @app_commands.command(description="Bans a member")
    @app_commands.describe(member="The member to ban")
    @app_commands.describe(reason="Reason of the ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self, interaction: discord.Interaction, member: discord.Member, reason: str
    ):

        await member.ban(reason=reason)
        await interaction.response.send_message(f"Banned {member}")
        chatlog_channel = self.bot.get_channel(1310776908908331040)

        embed = discord.Embed(
            title=f"The member <@{member.id}> has being banned",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )
        embed.add_field(name="**Reason**", value=reason, inline=False)
        embed.set_author(name=member.name, icon_url=member.display_avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await chatlog_channel.send(embed=embed)

    # Mute command
    @app_commands.command(description="Mute the member")
    @app_commands.describe(member="The member to mute")
    @app_commands.describe(time="For how long the member will stay muted")
    @app_commands.describe(reason="Reason of the mute")
    @app_commands.checks.has_permissions(ban_members=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        time: int,
        reason: str,
    ):

        time_muted = timedelta(minutes=time)
        await member.timeout(time_muted, reason=reason)

        await interaction.response.send_message(f"Muted {member}")
        chatlog_channel = self.bot.get_channel(1310776908908331040)

        embed = discord.Embed(
            title=f"The member {member.name} has being muted for {time}m",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )
        embed.add_field(name="**Reason**", value=reason, inline=False)
        embed.set_author(name=member.name, icon_url=member.display_avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await chatlog_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
