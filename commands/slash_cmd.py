import discord
import os
import json
from discord.ext import commands

with open('config.json') as config_file:
    config = json.load(config_file)

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Slash commands loaded for {self.bot.user.name}')

    @discord.app_commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World! 👋")

    @discord.app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000
        await interaction.response.send_message(f":evergreen_tree: **|** {self.bot.user.name} Latency is {latency:.2f}ms")

    @discord.app_commands.command(name="connection", description="Check if the bot can connect to the internet or not.")
    async def ping(self, interaction: discord.Interaction):
        hostname = config['pingserver']
        response = os.system("ping -n 1 " + hostname)
        if response == 0:
            await interaction.response.send_message(f":white_check_mark: **|** {self.bot.user.name} is able to connect to the internet. ({config['pingserver']})")
        else:
            await interaction.response.send_message(f":x: **|** {self.bot.user.name} is not able to connect to the internet. ({config['pingserver']})")
    
    @discord.app_commands.command(name="information", description="Check if the bot can connect to the internet or not.")
    async def ping(self, interaction: discord.Interaction):
        language = config['language']
        app_info = await self.bot.application_info()
        try:
            embed = discord.Embed(
                title="Bot Information",
                description=f"Bot: **{self.bot.user.mention}**.\nLanguge: **{language}**.\nBot Owner: **{app_info.owner.mention}**.\n\nCurrently Watching: **atleast 1** Servers.",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
            await interaction.response.send_message(f"Languge: {language}, Bot Owner: {app_info.owner.name}")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
        
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
