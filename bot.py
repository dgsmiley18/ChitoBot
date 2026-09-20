#!/usr/bin/env python3
import logging
import os
import sys
from datetime import datetime

import discord
import tomllib
from discord.ext import commands

# --- Configuration Loading ---
CONFIG_FILE = "config.toml"

if not os.path.exists(CONFIG_FILE):
    print(f"Error: Configuration file '{CONFIG_FILE}' not found.")
    print("Copy 'config.example.toml' to 'config.toml' and set up your variables.")
    sys.exit(1)

with open(CONFIG_FILE, "rb") as f:
    config = tomllib.load(f)

# Allow environment variables to override config values (for Docker)
TOKEN = os.getenv("DISCORD_TOKEN") or config.get("bot", {}).get("token")
PREFIX = config.get("bot", {}).get("prefix", "!")

if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("Error: Discord bot token is missing or not configured in config.toml.")
    sys.exit(1)

GUILD_ID = config.get("guild", {}).get("guild_id", 0)
WELCOME_CHANNEL_ID = config.get("features", {}).get("welcome_channel_id", 0)
AUTO_ROLE_ID = config.get("features", {}).get("auto_role_id", 0)
LOG_CHANNEL_ID = config.get("features", {}).get("log_channel_id", 0)

# --- Intents ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class ChitoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents)
        self.log_channel_id = LOG_CHANNEL_ID

    async def setup_hook(self):
        # Load extensions/cogs from the cogs directory
        if os.path.isdir("./cogs"):
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py") and not filename.startswith("__"):
                    cog_name = f"cogs.{filename[:-3]}"
                    try:
                        await self.load_extension(cog_name)
                        print(f"Loaded cog: {cog_name}")
                    except Exception as e:
                        print(f"Failed to load cog {cog_name}: {e}")

        # Synchronize application commands
        # If guild_id is provided, sync locally for instant updates during development
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild ID {GUILD_ID}")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s) globally.")


bot = ChitoBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    # Set presence based on server configuration
    if GUILD_ID:
        server = bot.get_guild(GUILD_ID)
        if server and server.member_count:
            await bot.change_presence(
                activity=discord.Activity(
                    name=f"{server.member_count} users",
                    type=discord.ActivityType.watching,
                )
            )
    else:
        await bot.change_presence(
            activity=discord.Activity(
                name=f"{len(bot.guilds)} servers",
                type=discord.ActivityType.watching,
            )
        )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    # Process standard prefix commands if any exist
    await bot.process_commands(message)


# --- Member Join & Leave Events ---
@bot.event
async def on_member_join(member: discord.Member):
    # Optional welcome message
    if WELCOME_CHANNEL_ID:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if isinstance(channel, discord.TextChannel):
            await channel.send(f"Hello {member.mention}, welcome to the server!")

    # Optional auto-role assignment
    if AUTO_ROLE_ID:
        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                print(f"[Warning] Bot lacks permissions to assign role '{role.name}'.")


@bot.event
async def on_member_remove(member: discord.Member):
    if WELCOME_CHANNEL_ID:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if isinstance(channel, discord.TextChannel):
            await channel.send(f"Goodbye {member.mention}, we will miss you!")


# --- Message Logging Events (Deleted & Edited) ---
@bot.event
async def on_message_delete(message: discord.Message):
    if not LOG_CHANNEL_ID or message.author.bot or not message.guild:
        return

    channel = message.guild.get_channel(LOG_CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        embed = discord.Embed(
            description=f"Message deleted in {message.channel.mention}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        content = message.content or "*[No text / attachment only]*"
        embed.add_field(name="Content", value=content, inline=False)
        embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {message.author.id}")
        await channel.send(embed=embed)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    # Ignore bot edits or events fired by embed expansions where content didn't change
    if not LOG_CHANNEL_ID or before.author.bot or not before.guild or before.content == after.content:
        return

    channel = before.guild.get_channel(LOG_CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        embed = discord.Embed(
            description=f"Message edited in {before.channel.mention} - [**Jump**]({before.jump_url})",
            color=discord.Color.yellow(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Before", value=before.content or "*[Empty]*", inline=False)
        embed.add_field(name="After", value=after.content or "*[Empty]*", inline=False)
        embed.set_author(name=str(before.author), icon_url=before.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {before.author.id}")
        await channel.send(embed=embed)


# --- Bot Startup ---
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
bot.run(TOKEN, log_handler=handler, log_level=logging.INFO)