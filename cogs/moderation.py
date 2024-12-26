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
        self, 
        interaction: discord.Interaction, 
        member: discord.Member | discord.User, 
        reason: str
    ):
            print(f"Ban command invoked for {member.name} with reason: {reason}")

            # Use defer to inform Discord that the command is being processed
            await interaction.response.defer(thinking=True)

            #Check if the member is in the server
            if member not in interaction.guild.members:
                await interaction.followup.send(f"The member {member} is not in the server and cannot be banned.")
                print(f"The member {member} is not in the server and cannot be banned.")
                return 

            # Send the ban message to the user
            if not member.dm_channel:
                await member.create_dm()

            try:
                await member.dm_channel.send(f"You have been banned from {member.guild.name} for the reason: {reason}")
                print(f"{member.name} was banned and the message was sent")
            except discord.Forbidden:
                await interaction.followup.send(f"It was not possible to send the message, maybe the user disabled their DMs.")
                print(f"It was not possible to send the message, maybe the user disabled their DMs.")
            except discord.NotFound:
                await interaction.followup.send(f"The member {member} is not in the server and cannot be banned.")
                print(f"The member {member} is not in the server and cannot be banned.")

            try:
                await interaction.guild.ban(user=member, reason=reason)
                await interaction.followup.send(f"{member} has been banned.")

                # chatlog_channel
                chatlog_channel = self.bot.get_channel(1310776908908331040)
                print(f"Chatlog channel: {chatlog_channel}")

                if chatlog_channel is None:
                    print("Chatlog channel not found or bot doesn't have access.")
                    return

                # Create the embed to send to the chatlog_channel
                embed = discord.Embed(
                    title=f"The member {member.name} has being banned",
                    color=discord.Color.red(),
                    timestamp=datetime.now(),
                )
                embed.add_field(name="**Reason**", value=reason, inline=False)
                embed.set_author(name=member.name, icon_url=member.display_avatar)
                embed.set_footer(text=f"User ID: {member.id}")

                await chatlog_channel.send(embed=embed)

            except discord.NotFound:
                await interaction.followup.send(f"The member {member} is not in the server or does not exist")
                print(f"The member {member} is not in the server and cannot be banned.")
            except Exception as e:
                await interaction.followup.send(f"An error occurred: {e}")
                print(f"An error occurred: {e}")

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

        # send the mute message to the user
        try:
            await member.send(f"You have been muted from {member.guild.name} for {time_muted} minutes for the reason: {reason}")
            print(f"{member.name} was muted and the message was sent")
        except discord.Forbidden:
            print(f"It was not possible to send the message, maybe the user disabled his dms")

            chatlog_channel = self.bot.get_channel(1310776908908331040)
            await member.timeout(time_muted, reason=reason)
            
            await interaction.response.send_message(f"{member} has being muted for {time}")

            embed = discord.Embed(
                title=f"The member {member.name} has being muted for {time}m",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
            embed.add_field(name="**Reason**", value=reason, inline=False)
            embed.set_author(name=member.name, icon_url=member.display_avatar)
            embed.set_footer(text=f"User ID: {member.id}")
            await chatlog_channel.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"an error was found {e}")
            await interaction.followup.send(f"an error was found {e}")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
