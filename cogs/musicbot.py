from enum import auto
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import pafy  
import random
from discord.ext import commands, tasks

import pafy
import urllib
import re
import time

class musicbot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = [] 
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        self.autoplay.start()
        self.loop = False

    @commands.command(pass_context = True)
    async def join(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You're not in a voice channel")
    
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        server = ctx.message.guild.voice_client
        self.queue.clear()
        await server.disconnect()

    @commands.command(pass_context = True)
    async def play(self, ctx, *url):

        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_client == None:
            voice_client = await voice.connect()
        else:
            await voice_client.move_to(channel)
        if voice_client.is_paused() and len(url) == 0:
            voice_client.resume()
            await ctx.send("Unpaused")
            return
        html = self.check_link(url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        

        if len(self.queue) == 0:
            song = pafy.new(video_ids[0]) 
            await ctx.send("**Now Playing** "+ song.title + "https://www.youtube.com/watch?v=" + video_ids[0] )
            self.queue.append([ctx.message.guild, video_ids, int(ctx.message.channel.id)]) 
            audio = song.getbest()  
           
            source = FFmpegPCMAudio(audio.url, **self.FFMPEG_OPTIONS)  
            voice_client.play(source)  

        else:
            self.queue.append([ctx.message.guild, video_ids, int(ctx.message.channel.id)])
            await ctx.send("The song has added to queue")


    @commands.command(pass_context = True)
    async def stop(self, ctx):
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_client:
            if voice_client.is_playing():
                voice_client.stop()
                self.queue.clear()

    @commands.command(pass_context = True)
    async def pause(self, ctx):
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_client:
            if voice_client.is_playing():
                voice_client.pause()
                await ctx.send("The song has been paused")
    
    @commands.command(pass_context = True)
    async def skip(self, ctx):
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice_client.stop()
        await ctx.send("The song has been skipped")

    

    @commands.command(pass_Context = True)
    async def queue(self, ctx):
        print("Panjang queue:", len(self.queue))
        if len(self.queue) >= 1:
            await ctx.send("**Queue**")
            for x, y in enumerate(self.queue):
                print(self.queue[x][1][0])
                myvid = pafy.new("https://www.youtube.com/watch?v=" + self.queue[x][1][0])
                await ctx.send(f"{x + 1}.  {myvid.title}")
        else:
            await ctx.send("Queuenya kosong")

    @commands.command(pass_Context = True)
    async def shuffle(self,ctx):
        random.shuffle(self.queue)
        await ctx.send("Queue sudah tershuffle")

    

    def check_link(self, data):
        if "v=" not in data[0]:
            keyword = "+".join(data)
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + keyword)
        else:
            search = data[0].split("v=")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search[1])
        return html
        

    @tasks.loop(seconds = 5)
    async def autoplay(self):
        if len(self.queue) == 0:
                return
        voice_client = discord.utils.get(self.client.voice_clients, guild=self.queue[0][0])
        if not voice_client.is_playing() and not voice_client.is_paused():
            self.queue.pop(0)
            if len(self.queue) == 0:
                return
            channel_id = self.queue[0][2]
            ctx = self.client.get_channel(channel_id)
            video_ids = self.queue[0][1]
            song = pafy.new(video_ids[0])
            await ctx.send("**Now Playing**" + song.title +" https://www.youtube.com/watch?v=" + video_ids[0])
            audio = song.getbest()  
            source = FFmpegPCMAudio(audio.url, **self.FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
            voice_client.play(source)  

def setup(client):
    client.add_cog(musicbot(client))



