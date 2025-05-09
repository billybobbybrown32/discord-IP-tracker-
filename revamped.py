import discord
import requests
from discord.ext import commands

TOKEN = ("YOUR_DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# try getting iP from api.ipify.org
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return {'ip': response.json().get('ip')}
    except Exception as e:
        return None  # fallback will handle

# if ipify fails, use ipinfo.io to get IP and location
def get_ipinfo_fallback():
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            'ip': data.get('ip'),
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country')
        }
    except Exception as e:
        return f"Failed to get IP info from both sources: {e}"

@bot.command(name='ipinfo')
async def ipinfo(ctx):
    ip_data = get_public_ip()

    if ip_data:
        msg = f"Public IP (via ipify): {ip_data.get('ip')}"
    else:
        ip_info = get_ipinfo_fallback()
        if isinstance(ip_info, dict):
            msg = (
                f"Fallback IP (via ipinfo.io): {ip_info.get('ip')}\n"
                f"Location: {ip_info.get('city')}, {ip_info.get('region')}, {ip_info.get('country')}"
            )
        else:
            msg = ip_info  # error message as string

    await ctx.send(msg)

bot.run(TOKEN)
