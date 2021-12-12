import asyncio
import random
import discord
import youtube_dl
from discord.ext import commands
import os
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        return data

        if 'entries' in data:
            # take first item from a playlist
            yt_queue += data['entries']
        else :
            yt_queue += data
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    


class Music(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self.voice_channel = None
        self.voice_client = None
        self.yt_queue = []
        self.is_checking = False
        self.ctx = None
        
    async def check_playing_status(self):
        await self.bot.wait_until_ready()
        self.is_checking = True
        while len(self.yt_queue):
            if self.voice_client is None:
                break
            if await self.not_playing():
                await self.next_song()
            await asyncio.sleep(5)
        self.is_checking = False

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        await self.ensure_voice(ctx)
        return
        if ctx.author.voice:
            self.voice_channel = ctx.author.voice.channel
            await self.voice_channel.connect()
            self.voice_client = ctx.voice_client
            print(type(self.voice_client))
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
            return
        
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(self.voice_channel)

        await self.channel.connect()




    @commands.command()
    async def play(self, ctx, *, url):
        """Play song"""

        if "我很好騙" in url:
            await ctx.send("你媽才很好騙")
            return

        if ctx.message.author.id == 786590754301935656 and random.random() > 0.5:
            await ctx.send("我只是一顆屎(搖頭晃腦")
            return
        
        
        data = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        if 'entries' in data:
            self.yt_queue += data['entries']
            if len(data['entries']) == 1:
                await ctx.send(f"Add {data['entries'][0].get('title')} to queue")
            else :
                await ctx.send(f"Add {len(data['entries'])} songs to queue")
        else :
            self.yt_queue += [data]
            await ctx.send(f"Add {data.get('title')} to queue")
        self.ctx = ctx
        if not self.is_checking:
            await self.check_playing_status()
            
    @commands.command()
    async def next(self, ctx):
        """Next song"""
        if not self.voice_client.is_paused():
            self.voice_client.pause()
        data =  await self.next_song()
        if data is None:
            return
    
    @commands.command()
    async def clear(self, ctx):
        """Clear queue"""
        self.yt_queue = []
        await ctx.send("Clear queue")
        await self.voice_client.stop()
    async def next_song(self):

        if len(self.yt_queue) == 0:
            return None
        data = self.yt_queue.pop(0)
        filename = data['url'] if True else ytdl.prepare_filename(data)
        
        player =  discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, **ffmpeg_options))
         
        self.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await self.ctx.send(f"Now playing : {data.get('title')}")
        return data

    @commands.command()
    async def queue(self, ctx):

        msg = "```"
        index = 1
        if len(self.yt_queue) == 0:
            msg += "There's no song in queue"
        else :
            for song in self.yt_queue:
                msg += f"{index:>3}  {song.get('title')} \n"
                index += 1
        msg += "```"
        if len(msg) != 0:
            await ctx.send(msg)


    @commands.command()
    async def pop(self, ctx, msg):
        """Use this to remove song from queue"""
        if not msg.isdigit():
            await ctx.send("請輸入正整數你這個白癡")
            return
        index = int(msg) - 1
        if index >= len(self.yt_queue):
            await ctx.send("沒這麼多歌你這個傻逼")
            return
        data = self.yt_queue.pop(index)
        await ctx.send(f"Remove {data.get('title')} from queue")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops"""
        await self.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        """Pause"""
        self.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resume"""
        self.voice_client.resume()


    @commands.command()
    async def check(self, ctx):
        print(f"Type of voice client : {type(self.voice_client)}")
        print(f"Type of voice channel : {type(self.voice_channel)}")
        
    async def not_playing(self):
        return not self.voice_client.is_playing() and not self.voice_client.is_paused()
    
    @play.before_invoke
    @next.before_invoke
    @clear.before_invoke
    @pop.before_invoke
    @stop.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    async def ensure_voice(self, ctx):
        
        if ctx.author.voice:
            self.voice_channel = ctx.author.voice.channel
        else:
            raise commands.CommandError("Author not connected to a voice channel.")
        
        if ctx.voice_client is None:
            await self.voice_channel.connect()
            
        self.voice_client = ctx.voice_client

        
def setup(bot):
    bot.add_cog(Music(bot))

