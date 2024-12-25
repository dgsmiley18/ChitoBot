import toml
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import logging

# Log
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
config = toml.load("config.toml")
token = config["config"]["token"]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Sync the commands
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    try:
        # load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")

        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands:")
        for command in synced:
            print(f"- {command.name} (ID: {command.id})")
    except Exception as e:
        print(f"Error during sync: {e}")
    # Activity
    server = bot.get_guild(1310733145779474563)
    await bot.change_presence(
        activity=discord.Activity(name=f"{server.member_count} users", type=3)
    )  # Displays 'Watching 3 users'


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

# When the member leaves the server
@bot.event
async def on_member_remove(member):
    welcome_channel = bot.get_channel(1310753679854272564)
    if welcome_channel:
        await welcome_channel.send(
            content=f"Goodbye <@{member.id}>, We will miss you!"
        )
    else:
        print("This channel does not exist.")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    print(f"Received interaction: {interaction.data}")


# Chat Log (Message Deleted)
@bot.event
async def on_message_delete(message):

    if message.author.bot:
        return
    
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
    
    if before.author.bot:
        return

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