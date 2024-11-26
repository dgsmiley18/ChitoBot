import os
import toml
import discord
from discord.ext import commands
from datetime import datetime
import logging

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
config = toml.load("config.toml")
token = config["config"]["token"]

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


# start the bot
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


# when a new member joins, it will send a message
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1310753679854272564)
    await channel.send(content=f"Hello {member.name}, Welcome to the server!")


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
    embed.add_field(name="**Aftere**", value=after.content, inline=False)
    embed.set_author(name=before.author, icon_url=before.author.display_avatar)
    embed.set_footer(text=f"User ID: {before.author.id}")
    await chatlog_channel.send(embed=embed)


bot.run(token, log_handler=handler, log_level="DEBUG")
