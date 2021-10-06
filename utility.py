import discord
from discord.ext import commands
import time
import asyncio
from datetime import datetime

class utility(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.client.launch_time = datetime.utcnow()
        print('Utility Cog status: loaded')
        
                
    @commands.command()
    async def invite(self, ctx):
        invite_embed=discord.Embed(title="So are you going to invite the bot or not?", color=discord.Colour.random(), description='Here are some basic links you need')
        invite_embed.add_field(name="Invite the bot", value="[Invite link - recommended](https://discord.com/api/oauth2/authorize?client_id=844272082720129035&permissions=4097309911&scope=bot)\n[Invite link - admin](https://discord.com/api/oauth2/authorize?client_id=844272082720129035&permissions=8&scope=bot)", inline=False)
        invite_embed.add_field(name="Join The support server", value="https://discord.gg/fSnYXMFXgM", inline=False)
        invite_embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/1Dniwd4_NaAOE3As_zxXgWNI_xGDw1cuE0QMgKtAyvs/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/844272082720129035/89d81fb3cfd8eb795faac574224a70de.png')
        await ctx.send(embed=invite_embed)

    @commands.command()
    async def ping(self, ctx):
        start=time.monotonic()
        m=await ctx.send("Pinging...")
        end=time.monotonic()
        overall=round((end-start)*1000,1)
        e=discord.Embed(title="Pinging...",description=f"Overall latency: {overall}ms")
        await asyncio.sleep(0.5)
        await m.edit(content=None,embed=e)
        await asyncio.sleep(0.5)
        ws=round(self.client.latency*1000,1)
        e.description=e.description+f"\nWebsocket latency: {ws}ms"
        await m.edit(embed=e)
        await asyncio.sleep(0.5)
        average=round((overall+ws)/2, 1)
        e.description=e.description+f"\nAverage latency: {average}ms"
        e.title="Pong! :ping_pong:"
        e.color=discord.Colour.random()
        await m.edit(embed=e)

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

    @commands.command(aliases=['TIMER', 'remind', 'REMIND'])
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def timer(self, ctx, timeInput, *, title='Timer'):
        try:
            try:
                time = int(timeInput)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
                time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            if time > 86400:
                await ctx.send("I cant sit here and to timers all day")
                return
            if time <= 0:
                await ctx.send("Timers don\'t go into negatives :/")
                return
            if time >= 3600:
                embed = discord.Embed(
                    title=f'{title}',
                    description=f"{time//3600} hours {time%3600//60} minutes {time%60} seconds",
                    color=discord.Colour.random()
                )
                embed.set_footer(text='React with ⏰ to be notified')
                message = await ctx.reply(embed=embed, mention_author=True)
                await message.add_reaction('⏰')
            elif time >= 60:
                embed = discord.Embed(
                    title=f'{title}',
                    description=f"{time//60} minutes {time%60} seconds",
                    color=discord.Color.random()
                )
                embed.set_footer(text='React with ⏰ to be notified')
                message = await ctx.reply(embed=embed, mention_author=True)
                await message.add_reaction('⏰')
            elif time < 60:
                embed = discord.Embed(
                    title=f'{title}',
                    description=f'{time} seconds',
                    color=discord.Color.random()
                )
                embed.set_footer(text='React with ⏰ to be notified')
                message = await ctx.reply(embed=embed, mention_author=True)
                await message.add_reaction('⏰')
            while True:
                try:
                    await asyncio.sleep(6)
                    time -= 6
                    if time >= 3600:
                        embed = discord.Embed(
                            title=f'{title}',
                            description=f"{time//3600} hours {time%3600//60} minutes {time%60} seconds",
                            color=discord.Color.random()
                        )
                        embed.set_footer(text='React with ⏰ to be notified')
                        await message.edit(embed=embed)
                    elif time >= 60:
                        embed = discord.Embed(
                            title=f'{title}',
                            description=f"{time//60} minutes {time%60} seconds",
                            color=discord.Color.random()
                        )
                        embed.set_footer(text='React with ⏰ to be notified')
                        await message.edit(embed=embed)
                    elif time < 60:
                        embed = discord.Embed(
                            title=f'{title}',
                            description=f"{time} seconds",
                            color=discord.Color.random()
                        )
                        embed.set_footer(text='React with ⏰ to be notified')
                        await message.edit(embed=embed)
                    if time <= 0:
                        embed = discord.Embed(
                            title=f'{title}',
                            description='Time\'s up!',
                            color=0x2e3135
                        )
                        await message.edit(embed=embed)
                        m = await ctx.channel.fetch_message(message.id)
                        list_thingy = []
                        output_list_thingy = []
                        reactants = await m.reactions[0].users().flatten()
                        reactants.pop(reactants.index(self.client.user))
                        for user in reactants:
                            list_thingy.append(user.id)
                            x = '<@!' + str(user.id) + '>' 
                            output_list_thingy.append(x)
                        if output_list_thingy != []:
                            final = ', '.join(map(str, output_list_thingy))
                            return await ctx.send(f'The timer for **{title}** has ended!\n{final}')
                        else:
                            return await ctx.send(f'The timer for **{title}** has ended!')
                except:
                    break
        except:
            await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time **{timeInput}**....")

def setup(client):
    client.add_cog(utility(client))