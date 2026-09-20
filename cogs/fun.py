import discord
from discord import app_commands
from discord.ext import commands


class Fun(commands.Cog):
    """Cog responsible for fun and informational user utility commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- Ping Command ---
    @app_commands.command(name="ping", description="Check the bot latency.")
    async def ping(self, interaction: discord.Interaction):
        # Latency in milliseconds
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: `{latency}ms`")

    # --- Profile Picture Command ---
    @app_commands.command(name="pfp", description="Show the profile picture of a member.")
    @app_commands.describe(member="The member whose profile picture you want to view")
    async def pfp(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None,
    ):
        target = member or interaction.user

        embed = discord.Embed(
            title=f"Profile Picture - {target.display_name}",
            color=target.color if isinstance(target, discord.Member) else discord.Color.blurple(),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_image(url=target.display_avatar.url)
        embed.set_footer(text=f"User ID: {target.id}")
        await interaction.response.send_message(embed=embed)

    # --- User Information Command ---
    @app_commands.command(name="userinfo", description="Display detailed information about a member.")
    @app_commands.describe(member="The member to view information about.")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None,
    ):
        # Default to interaction user if no target provided
        target = member or interaction.user

        if not isinstance(target, discord.Member):
            await interaction.response.send_message(
                "This command can only be used within a server to display member information.",
                ephemeral=True,
            )
            return

        # Unix timestamps for dynamic Discord relative formatting
        account_created_unix = int(target.created_at.timestamp())
        join_date_unix = int(target.joined_at.timestamp()) if target.joined_at else None

        account_created = f"<t:{account_created_unix}:F> (<t:{account_created_unix}:R>)"
        join_date = f"<t:{join_date_unix}:F> (<t:{join_date_unix}:R>)" if join_date_unix else "N/A"

        # Format roles (excluding @everyone)
        roles = [role.mention for role in target.roles[1:]]
        roles.reverse()  # Show higher roles first
        roles_display = ", ".join(roles) if roles else "None"

        # Truncate if exceeds Discord embed field limit (1024 characters)
        if len(roles_display) > 1000:
            roles_display = f"{roles_display[:990]}... and {len(roles) - 10} more"

        embed = discord.Embed(
            color=target.color,
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(name=str(target), icon_url=target.display_avatar.url)
        embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="Username", value=target.name, inline=True)
        embed.add_field(name="Display Name", value=target.display_name, inline=True)
        embed.add_field(name="ID", value=str(target.id), inline=True)

        embed.add_field(name="Account Created", value=account_created, inline=False)
        embed.add_field(name="Joined Server", value=join_date, inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]", value=roles_display, inline=False)

        embed.set_footer(text=f"Requested by {interaction.user.name}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))