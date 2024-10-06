import discord
import os
import json
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from discord.ext import commands

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Map activity types to Discord activity types
activity_type_mapping = {
    "playing": discord.ActivityType.playing,
    "streaming": discord.ActivityType.streaming,
    "listening": discord.ActivityType.listening,
    "watching": discord.ActivityType.watching,
    "competing": discord.ActivityType.competing
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class CogHandler(FileSystemEventHandler):
    def __init__(self, bot):
        self.bot = bot

    async def sync_commands(self):
        await self.bot.tree.sync()
        print("Slash commands synced.")

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'Reloading {event.src_path}')
            loop = self.bot.loop
            loop.create_task(self.reload_cog(event.src_path))

    async def reload_cog(self, path):
        cog_name = os.path.basename(path)[:-3]
        try:
            channel = self.bot.get_channel(1291398870915612713)
            await channel.send(f'Reloading {os.path.basename(path)}')

            await self.bot.unload_extension(f'commands.{cog_name}')
            await self.bot.load_extension(f'commands.{cog_name}')
            await self.sync_commands()
        except Exception as e:
            channel = self.bot.get_channel(1291398870915612713)
            await channel.send(f'I failed to reload {cog_name}. Here’s error: {e}')
            print(f'Failed to reload {cog_name}: {e}')

async def load_cogs():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

@bot.event
async def on_ready():
    activity_type = activity_type_mapping.get(config['activity_type'], discord.ActivityType.playing)
    activity = discord.Activity(type=activity_type, name=config['activity_name'])
    await bot.change_presence(activity=activity)

    print(f'We have logged in as {bot.user}')

    event_handler = CogHandler(bot)
    observer = Observer()
    observer.schedule(event_handler, path='./commands', recursive=False)
    observer.start()

    await load_cogs()
    await bot.tree.sync()
    await event_handler.sync_commands()

bot.run(config['token'])
