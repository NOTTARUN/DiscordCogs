import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
from io import StringIO


class imagegen(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('ImageGen Cog status: loaded')
      
    @commands.command()
    async def chad(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author 
        trash = Image.open("chad.jpg")
        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((300,300))
        trash.paste(pfp, (180, 85))
        trash.save("chad_profile.jpg")
        await ctx.send(file = discord.File("chad_profile.jpg"))
    
    @commands.command()
    async def trash(self, ctx, user: discord.Member = None):
        if user == None:
           user = ctx.author 
        trash = Image.open("trash.jpg")
        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((300,300))
        trash.paste(pfp, (996, 588))
        trash.save("profile.jpg")
        await ctx.send(file = discord.File("trash_profile.jpg"))

def setup(client):
    client.add_cog(imagegen(client))