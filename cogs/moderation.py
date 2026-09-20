from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    """Cog responsible for moderation actions such as purge, ban, and mute."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _send_log(self, guild: discord.Guild, embed: discord.Embed) -> None:
        """Helper to send moderation logs to the configured channel."""
        log_channel_id = getattr(self.bot, "log_channel_id", 0)
        if not log_channel_id:
            return

        channel = guild.get_channel(log_channel_id)
        if isinstance(channel, discord.TextChannel):
            await channel.send(embed=embed)

    # --- Purge Command ---
    @app_commands.command(name="purge", description="Clears a specified number of messages.")
    @app_commands.describe(limit="Number of messages to delete", reason="Reason for purging messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, limit: int, reason: str = "No reason provided"):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.channel, (discord.TextChannel, discord.Thread)):
            await interaction.followup.send("This channel does not support message purging.", ephemeral=True)
            return

        if limit < 1 or limit > 100:
            await interaction.followup.send("Please provide a limit between 1 and 100.", ephemeral=True)
            return

        try:
            deleted = await interaction.channel.purge(limit=limit, reason=reason)
            await interaction.followup.send(
                f"Successfully deleted {len(deleted)} message(s). Reason: {reason}",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.followup.send("Missing permissions to delete messages in this channel.", ephemeral=True)
        except Exception as error:
            await interaction.followup.send(f"An unexpected error occurred: {error}", ephemeral=True)

    # --- Ban Command ---
    @app_commands.command(name="ban", description="Bans a member or user from the server.")
    @app_commands.describe(user="The member or user to ban", reason="Reason for the ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.Member | discord.User,
        reason: str = "No reason provided",
    ):
        await interaction.response.defer(thinking=True)

        if not interaction.guild:
            await interaction.followup.send("This command can only be executed within a server.")
            return

        # Prevent attempting to ban hierarchy superiors or the bot itself
        if isinstance(user, discord.Member):
            if user.top_role >= interaction.guild.me.top_role:
                await interaction.followup.send("Cannot ban this member due to role hierarchy constraints.")
                return
            if user.id == interaction.user.id:
                await interaction.followup.send("You cannot ban yourself.")
                return

        # Attempt to notify the target via DM prior to banning
        try:
            await user.send(f"You have been banned from **{interaction.guild.name}**. Reason: {reason}")
        except (discord.Forbidden, discord.HTTPException):
            pass  # Ignore if DMs are closed or delivery fails

        # Execute ban action using a Snowflake reference to bypass static typing warnings
        try:
            await interaction.guild.ban(discord.Object(id=user.id), reason=reason)
            await interaction.followup.send(f"Successfully banned **{user}**.")

            # Create and dispatch log embed
            embed = discord.Embed(
                title=f"Member Banned: {user}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow(),
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            embed.set_author(name=str(user), icon_url=user.display_avatar.url)
            embed.set_footer(text=f"User ID: {user.id}")

            await self._send_log(interaction.guild, embed)

        except discord.Forbidden:
            await interaction.followup.send("Failed to execute ban: insufficient bot permissions.")
        except Exception as error:
            await interaction.followup.send(f"An error occurred while executing the ban: {error}")

    # --- Mute (Timeout) Command ---
    @app_commands.command(name="mute", description="Applies a temporary timeout to a member.")
    @app_commands.describe(member="The member to mute", duration_minutes="Duration of the mute in minutes", reason="Reason for the mute")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration_minutes: int,
        reason: str = "No reason provided",
    ):
        await interaction.response.defer(thinking=True)

        if not interaction.guild:
            await interaction.followup.send("This command can only be executed within a server.")
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.followup.send("Cannot mute this member due to role hierarchy constraints.")
            return

        duration = timedelta(minutes=duration_minutes)

        # Notify via direct message before applying the timeout
        try:
            await member.send(
                f"You have been muted in **{interaction.guild.name}** for {duration_minutes} minute(s). Reason: {reason}"
            )
        except (discord.Forbidden, discord.HTTPException):
            pass

        try:
            await member.timeout(duration, reason=reason)
            await interaction.followup.send(f"Successfully muted **{member}** for {duration_minutes} minute(s).")

            # Create and dispatch log embed
            embed = discord.Embed(
                title=f"Member Muted: {member}",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow(),
            )
            embed.add_field(name="Duration", value=f"{duration_minutes} minute(s)", inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            embed.set_author(name=str(member), icon_url=member.display_avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")

            await self._send_log(interaction.guild, embed)

        except discord.Forbidden:
            await interaction.followup.send("Failed to apply timeout: insufficient permissions.")
        except Exception as error:
            await interaction.followup.send(f"An error occurred while muting: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))