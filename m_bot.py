from discord.ext import commands
from youtube_dl import YoutubeDL
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('TOKEN')

bot = commands.Bot(command_prefix="[")

players = {}
@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()
@bot.command(pass_context=True)
async def play(ctx, url):

    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
bot.run(TOKEN)
