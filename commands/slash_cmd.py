import discord
import os
import json
import requests
from discord.ext import commands

with open('config.json') as config_file:
    config = json.load(config_file)

API_URL = config['API_URL']
API_KEY = config['API_KEY']

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def fetch_server_ids():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [server['attributes']['identifier'] for server in data['data']]
    else:
        return []

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

    @discord.app_commands.command(name="connection", description="Check internet connectivity.")
    async def connection(self, interaction: discord.Interaction):
        hostname = config['pingserver']
        response = os.system("ping -n 1 " + hostname)
        if response == 0:
            await interaction.response.send_message(f":white_check_mark: **|** {self.bot.user.name} can connect to the internet. ({config['pingserver']})")
        else:
            await interaction.response.send_message(f":x: **|** {self.bot.user.name} cannot connect to the internet. ({config['pingserver']})")
    
    @discord.app_commands.command(name="information", description="Get bot information.")
    async def information(self, interaction: discord.Interaction):
        language = config['language']
        app_info = await self.bot.application_info()
        try:
            GetServerCount = requests.get(API_URL, headers=headers)
            GetServerCount.raise_for_status()

            data = GetServerCount.json()
            server_count = len(data['data'])

            embed = discord.Embed(
                title="Bot Information",
                description=f"Bot: **{self.bot.user.mention}**.\nBot Owner: **{app_info.owner.mention}**.\n\nServers: **{server_count}** Servers.\n",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

    @discord.app_commands.command(name="servers", description="List all servers.")
    async def servers(self, interaction: discord.Interaction):
        try:
            GetServers = requests.get(API_URL, headers=headers)
            GetServers.raise_for_status()

            data = GetServers.json()
            Servers = data.get('data', [])

            embed = discord.Embed(
                title="Pteroller - All Available Servers.",
                color=discord.Color.blue()
            )
            if Servers:
                for server in Servers:
                    server_id = server.get('attributes', {}).get('identifier', 'Unknown Server ID')
                    server_name = server['attributes'].get('name', 'Unknown Server Name')
                    server_status = server['attributes'].get('status', 'Unknown Status')
                    server_memory = server['attributes'].get('limits', {}).get('memory', 'Unknown Memory')

                    embed.add_field(
                        name=f"{server_name}",
                        value=f"Server ID: **{server_id}**\nStatus: **{server_status}**\nMax Memory: **{server_memory}MB**",
                        inline=False
                    )
            else:
                embed = discord.Embed(
                    title="Pteroller",
                    description="No servers found.",
                    color=discord.Color.red()
                )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

    @discord.app_commands.command(name="restart", description="Restart a server.")
    async def restart(self, interaction: discord.Interaction, server_id: str):
        restart_url = f"{API_URL}/servers/{server_id}/power"
        json_payload = {
            "signal": "restart"
        }
        response = requests.post(restart_url, headers=headers, json=json_payload)
        if response.status_code == 204:
            await interaction.response.send_message(f"Server {server_id} is restarting.")
        else:
            await interaction.response.send_message(f"Failed to restart server {server_id}. Status Code: {response.status_code}")

    @restart.autocomplete('server_id')
    async def server_id_autocomplete(self, interaction: discord.Interaction, current: str):
        server_ids = fetch_server_ids()
        return [discord.app_commands.Choice(name=server_id, value=server_id) for server_id in server_ids if current.lower() in server_id.lower()]
    
    @discord.app_commands.command(name="kill", description="Kill a server.")
    async def kill(self, interaction: discord.Interaction, server_id: str):
        kill_url = f"{API_URL}/servers/{server_id}/power"
        json_payload = {
            "signal": "kill"
        }
        response = requests.post(kill_url, headers=headers, json=json_payload)
        if response.status_code == 204:
            await interaction.response.send_message(f"Killing {server_id}.")
        else:
            await interaction.response.send_message(f"Failed to kill server {server_id}. Status Code: {response.status_code}")

    @kill.autocomplete('server_id')
    async def server_id_autocomplete(self, interaction: discord.Interaction, current: str):
        server_ids = fetch_server_ids()
        return [discord.app_commands.Choice(name=server_id, value=server_id) for server_id in server_ids if current.lower() in server_id.lower()]
    
    @discord.app_commands.command(name="stop", description="Stop a server.")
    async def stop(self, interaction: discord.Interaction, server_id: str):
        stop_url = f"{API_URL}/servers/{server_id}/power"
        json_payload = {
            "signal": "stop"
        }
        response = requests.post(stop_url, headers=headers, json=json_payload)
        if response.status_code == 204:
            await interaction.response.send_message(f"Stopping Server {server_id}.")
        else:
            await interaction.response.send_message(f"Failed to stop server {server_id}. Status Code: {response.status_code}")

    @stop.autocomplete('server_id')
    async def server_id_autocomplete(self, interaction: discord.Interaction, current: str):
        server_ids = fetch_server_ids()
        return [discord.app_commands.Choice(name=server_id, value=server_id) for server_id in server_ids if current.lower() in server_id.lower()]
    
    @discord.app_commands.command(name="start", description="Start a server.")
    async def start(self, interaction: discord.Interaction, server_id: str):
        start_url = f"{API_URL}/servers/{server_id}/power"
        json_payload = {
            "signal": "start"
        }
        response = requests.post(start_url, headers=headers, json=json_payload)
        if response.status_code == 204:
            await interaction.response.send_message(f"Starting Server {server_id}.")
        else:
            await interaction.response.send_message(f"Failed to Start server {server_id}. Status Code: {response.status_code}")

    @start.autocomplete('server_id')
    async def server_id_autocomplete(self, interaction: discord.Interaction, current: str):
        server_ids = fetch_server_ids()
        return [discord.app_commands.Choice(name=server_id, value=server_id) for server_id in server_ids if current.lower() in server_id.lower()]

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
