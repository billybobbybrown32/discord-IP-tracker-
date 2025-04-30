import discord
import requests
from discord.ext import commands

# Your bot's token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Create bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# IPinfo API endpoint
IPINFO_URL = 'https://ipinfo.io/'

# Function to get the IP information
def get_ip_info(ip):
    try:
        response = requests.get(f'{IPINFO_URL}{ip}/json')
        return response.json()
    except Exception as e:
        return f"Error fetching IP info: {e}"

# Command to get device and IP info
@bot.command(name='ipinfo')
async def ipinfo(ctx):
    # Get the IP address of the sender (user who triggered the command)
    user_ip = ctx.author.ip # NOTE: This won't work directly, you'll need a custom proxy server for real IP
    ip_details = get_ip_info(user_ip)

    # Send a message with the device and IP info
    if isinstance(ip_details, dict):
        msg = f"Device: {ctx.author}\nIP: {user_ip}\nLocation: {ip_details.get('city')}, {ip_details.get('region')}, {ip_details.get('country')}"
    else:
        msg = ip_details

    await ctx.send(msg)

# Start the bot
bot.run(TOKEN)
