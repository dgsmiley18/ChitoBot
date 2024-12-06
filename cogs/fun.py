import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ping command
    @app_commands.command(description="Ping!")
    async def ping(self, interaction: discord.Interaction):

        await interaction.response.send_message("Pong!")

    # Show Profile Picture command
    @app_commands.command(description="Show the profile picture from a member")
    @app_commands.describe(member="The member to show the pfp")
    async def pfp(self, interaction: discord.Interaction, member: discord.Member):

        embed = discord.Embed(
            title=f"Profile Picture from {member.name}",
            color=member.color,
            timestamp=datetime.now(),
        )
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"User ID: {member.id}")
        await interaction.response.send_message(embed=embed)

    # Userinfo command
    @app_commands.command(description="Show the user information")
    @app_commands.describe(member="The member to show the info")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):

        # timestamps UNIX
        account_created_unix = int(member.created_at.timestamp())
        join_date_unix = int(member.joined_at.timestamp()) if member.joined_at else None

        # convert to <t:timestamp:F>
        account_created = f"<t:{account_created_unix}:F>"
        join_date = f"<t:{join_date_unix}:F>" if join_date_unix else "N/A"

        # get member roles
        role_names = ", ".join([role.mention for role in member.roles[1:]])

        embed = discord.Embed(
            color=member.color,
            timestamp=datetime.now(),
        )
        embed.add_field(name="**ID**", value=member.id, inline=True)
        embed.add_field(name="**Nick**", value=member.name, inline=True)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Account Created", value=account_created, inline=False)
        embed.add_field(name="Join Date", value=join_date, inline=False)
        embed.add_field(name=f"Roles [{len(member.roles[1:])}]", value=role_names)
        embed.set_author(name=member.name, icon_url=member.display_avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
