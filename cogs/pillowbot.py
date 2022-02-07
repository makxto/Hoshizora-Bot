import discord
from discord import client
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

class pillowbot(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def jelek(self, ctx, user: discord.Member = None):
        if  user == None:
            user = ctx.author

        jelek = Image.open("assets/jelek.jpg")

        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((510,477))

        jelek.paste(pfp, (270,278))

        jelek.save("assets/profile.jpg")
        await ctx.send(file = discord.File("assets/profile.jpg"))

    @commands.command()
    async def katain(self, ctx , user:discord.Member=None,*,text = "apaan"):
        if user == None:
            user = ctx.author
        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((510,477))
        img = Image.open("assets/black.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("assets/Poppins.ttf", 42)
        draw.text((150,150), text, (255,255,255), font=font)
        img.paste(pfp, (270,278))
        img.save("assets/text.png")
        await ctx.send(file = discord.File("assets/text.png"))

def setup(client):
    client.add_cog(pillowbot(client))