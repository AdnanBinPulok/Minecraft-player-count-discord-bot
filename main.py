import discord
from discord.ext import commands
import asyncio
import datetime
import requests
import json


class config():
    with open('./settings/config.json','r') as f:
        config_data = json.load(f)
    
    token=config_data.get('token',None)
    prefix = config_data.get('prefix',None)


    server_ip = "play.minehouse.fun"

    voice_count_channel_id=1110544798764511343



bot = commands.Bot(command_prefix=config.prefix,intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("-"*40)
    print(f"The bot is ready.")
    print(f"Name: {bot.user.name}")
    print("-"*40)
    await voice_channel_counter()

async def voice_channel_counter():
    while True:
        try:
            channel = bot.get_channel(config.voice_count_channel_id)

            response = requests.get(f"https://api.mcsrvstat.us/3/{config.server_ip}")

            if response.status_code != 200:
                await channel.edit(name=f"Server Offline")
            else:
                data = response.json()
                if data['online'] != True:
                    await channel.edit(name=f"Server Offline")
                    continue 
                
                online_player=data['players']['online']
                max_players=data['players']['max']
                await channel.edit(name=f"Online: {online_player}/{max_players}")
        except:
            None
        await asyncio.sleep(30)



bot.run(token=config.token)