import discord
from discord.ext import commands
import asyncio

class calculators(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Calculator Cog status: loaded')

    @commands.command(aliases=['bc', 'bankcalc'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bankcalculate(self, ctx, ExpInput, PresInput):
        embed=discord.Embed(
            title='Calculating Bankspace', 
            description='Just a sec...', 
            color=0xC0382B
        )
        message = await ctx.send(embed=embed) 
        await asyncio.sleep(1)

        try:
            try:
                ExpInputInt = int(ExpInput)
                PresInputInt = int(PresInput)
            except:
                ExpInputInt = int(ExpInput)  

            if ExpInputInt in range(0, 5000) & PresInputInt in range(0, 19):
                ExpLevel = ExpInputInt * 100
                PrestigeLevel = PresInputInt * 27.5
                PrestigeEXP = PrestigeLevel + 55
                BankSpace = round(PrestigeEXP * ExpLevel)
                number_with_commas_bank_space = '{:,}'.format(BankSpace)
                embed=discord.Embed(
                    title=' Bank Space Calculator',
                    color=0x2ECC70
                )
                embed.add_field(name='Experience Level\n', value=f'```fix\n {ExpInputInt}```', inline=True)
                embed.add_field(name='Prestige Level\n', value=f'```prolog\n {PresInputInt}```', inline=True)
                embed.add_field(name='Estimated BankSpace:\n', value=f'```ini\n[{number_with_commas_bank_space}]```', inline=True)
                embed.set_footer(text='Run Dinvite to invite me')
                await message.edit(embed=embed)
                                
        except:
            embed=discord.Embed(
                title='Uh oh', 
                description='Something went wrong please try again',
                color=0xC0382B
            )
            embed.set_footer(text='Join our support server for more assistance')
            await message.edit(embed=embed)

    @commands.command(aliases=['tc', 'taxcalc'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def taccalculate(self, ctx, taximput):
        embed=discord.Embed(
            title='Calculating Bank Space', 
            description='Just a sec...', 
            color=0xC0382B
        )
        message = await ctx.send(embed=embed) 
        await asyncio.sleep(1)

        try:
            try:
                taximputInt = int(taximput)  
            except:
                try:
                    convertTaximputList = {'k':1000, 'm':1000000, 'b':1000000000, 'K':1000, 'M':1000000, 'B':1000000000}
                    taximputInt = int(taximput[:-1]) * convertTaximputList[taximput[-1]]
                except:
                    try:
                        e1TaximputList = {'e0':1, 'e1':10, 'e2':100, 'e3':1000, 'e4':10000, 'e5':100000, 'e6':1000000, 'e7':10000000, 'e8':100000000, 'e9':1000000000}
                        taximputInt = int(taximput[:-2]) * e1TaximputList[taximput[-2:]]
                    except:
                        e2TaximputList = {'e10':10000000000, 'e11':100000000000, 'e12':1000000000000}
                        taximputInt = int(taximput[:-3]) * e2TaximputList[taximput[-3:]]

def setup(client):
    client.add_cog(calculators(client))
