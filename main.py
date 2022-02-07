import discord
from discord import client
from discord.ext import commands
import cogs.musicbot as musicbot
import cogs.pillowbot as pillowbot
import cogs.fernetbot as fernetbot
import random

from io import BytesIO


cogs = [musicbot, pillowbot, fernetbot]

client= commands.Bot(command_prefix="sen") 

intents = discord.Intents.all()

for i in range (len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print("The bot is online!!")

@client.command()
async def hello(ctx):
    await ctx.send(f"hello! {ctx.author.name}")

@client.command()
async def greet(ctx):
    await ctx.send(f"greetings {ctx.author.name}")
    
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)} ms')

@client.command()
async def roll(ctx):
    await ctx.send(random.randint(1,100))

@client.command()
async def echo(ctx, amount:int, *, message):
    for i in range(amount):
        await ctx.send(message)

@client.command()
async def dev(ctx):
    embed=discord.Embed(title= "Senritsu", 
    url="https://github.com/makxto",description="This Bot is created for fun by Senritsu and Dont Forget to Follow My GitHub", color=0xFF5733)
    await ctx.send(embed=embed)
    


@client.command()
async def bin(ctx, message):
    await ctx.send(f'Binary anda adalah {bin (message)}')



client.run("YOUR TOKEN HERE")