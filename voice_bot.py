import asyncio

import discord
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands
import os


TOKEN = os.getenv("TOKEN")


bot = commands.Bot(command_prefix=commands.when_mentioned_or("["),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
@bot.command()
async def reload(ctx):
    bot.reload_extension('music')
bot.load_extension('music')
bot.run(TOKEN)
