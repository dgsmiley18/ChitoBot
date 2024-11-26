import toml
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import logging

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
config = toml.load("config.toml")
token = config["config"]["token"]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Purge messages command
@app_commands.command(description="Clear the messages")
@app_commands.describe(limit="number of messages")
@app_commands.describe(reason="Reason for the purge")
async def purge(interaction: discord.Interaction, limit: int, reason: str):

    await interaction.response.defer(ephemeral=True)
    try:
        deleted = await interaction.channel.purge(limit=limit, reason=reason)
        await interaction.followup.send(f"Deleted {len(deleted)} message(s) for the reason: {reason}")
    except Exception as e:
        await interaction.followup.send(f"an error was found {e}")


# Ban member command
@app_commands.command(description="Bans a member")
@app_commands.describe(member="The member to ban")
@app_commands.describe(reason="Reason of the ban")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):

    await member.ban(reason=reason)
    await interaction.response.send_message(f"Banned {member}")
    chatlog_channel = bot.get_channel(1310776908908331040)

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
async def mute(interaction: discord.Interaction, member: discord.Member, time: int, reason: str):
    
    time_muted = timedelta(minutes=time)
    await member.timeout(time_muted, reason=reason)

    await interaction.response.send_message(f"Muted {member}")
    chatlog_channel = bot.get_channel(1310776908908331040)

    embed = discord.Embed(
        title=f"The member {member.name} has being muted for {time}m",
        color=discord.Color.red(),
        timestamp=datetime.now(),
    )
    embed.add_field(name="**Reason**", value=reason, inline=False)
    embed.set_author(name=member.name, icon_url=member.display_avatar)
    embed.set_footer(text=f"User ID: {member.id}")
    await chatlog_channel.send(embed=embed)

# ping command
@app_commands.command(description="Ping!")
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message("Pong!")

# Show Profile Picture command
@app_commands.command(description="Show the profile picture from a member")
@app_commands.describe(member="The member to show the pfp")
async def pfp(interaction: discord.Interaction, member: discord.Member):
        
    embed = discord.Embed(
        title=f"Profile Picture from {member.name}",
        color=member.color,
        timestamp=datetime.now(),
    )
    embed.set_image(url=member.display_avatar.url)
    embed.set_footer(text=f"User ID: {member.id}")
    await interaction.response.send_message(embed=embed)

# Sync the commands
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    try:
        bot.tree.add_command(ping)
        bot.tree.add_command(ban)
        bot.tree.add_command(purge)
        bot.tree.add_command(mute)
        bot.tree.add_command(pfp)
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands:")
        for command in synced:
            print(f"- {command.name} (ID: {command.id})")
    except Exception as e:
        print(f"Error during sync: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


# When the member joins the server
@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(1310753679854272564)
    if welcome_channel:
        await welcome_channel.send(
            content=f"Hello <@{member.id}>, Welcome to the server!"
        )

        role = member.guild.get_role(1310738184233287720)
        if role:
            await member.add_roles(role)
            print(f"Role {role.name} added to {member.name}.")
        else:
            print(f"Role not found for {member.name}.")
    else:
        print("This channel does not exist.")


# Chat Log (Message Deleted)
@bot.event
async def on_message_delete(message):
    chatlog_channel = bot.get_channel(1310776908908331040)
    embed = discord.Embed(
        description=f"Message deleted in <#{message.channel.id}>",
        color=discord.Color.red(),
        timestamp=datetime.now(),
    )
    embed.add_field(name="**Content**", value=message.content, inline=False)
    embed.set_author(name=message.author, icon_url=message.author.display_avatar)
    embed.set_footer(text=f"User ID: {message.author.id}")
    await chatlog_channel.send(embed=embed)


# Chat Log (Message Edited)
@bot.event
async def on_message_edit(before, after):
    chatlog_channel = bot.get_channel(1310776908908331040)
    jump_url = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
    embed = discord.Embed(
        description=f"Message edited in <#{before.channel.id}> - [**Jump to message**]({jump_url})",
        color=discord.Color.yellow(),
        timestamp=datetime.now(),
    )
    embed.add_field(name="**Before**", value=before.content, inline=False)
    embed.add_field(name="**After**", value=after.content, inline=False)
    embed.set_author(name=before.author, icon_url=before.author.display_avatar)
    embed.set_footer(text=f"User ID: {before.author.id}")
    await chatlog_channel.send(embed=embed)


bot.run(token, log_handler=handler, log_level="DEBUG")
