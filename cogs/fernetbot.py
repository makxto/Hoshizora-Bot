import discord
from discord import client
from discord.ext import commands

from cryptography.fernet import Fernet

class fernetbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def encrypt(self, ctx):
        user = ctx.author
        await user.send("Please enter the message to decrypt.")
        response = await commands.wait_for('message') # , check=message_check(channel=ctx.author.dm_channel))
        message = response.content
        encoded = message.encode()
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted = f.encrypt(encoded)
        await ctx.author.send("This is your encrypted message:")
        await ctx.author.send(encrypted.decode())
        await ctx.author.send("This is the key to decrypt the message:")
        await ctx.author.send(key.decode())


    @commands.command()
    async def decrypt(self, ctx):
        user = ctx.author
        await user.send("Please enter the encrypted message.")
        response = await commands.wait_for('message') # , check=message_check(channel=ctx.author.dm_channel))
        encrypted = response.content.encode()
        await user.send("Please enter the decryption key:")
        response = await commands.wait_for('message') # , check=message_check(channel=ctx.author.dm_channel))
        key = response.content.encode()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
        decoded = decrypted.decode()
        await user.send(decoded)
        print(decoded)
    
def setup(client):
    client.add_cog(fernetbot(client))