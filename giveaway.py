import re
import random
import asyncio

import discord
from discord.ext import commands

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)

async def GetMessage(
    client, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100
):
    """
    This function sends an embed containing the params and then waits for a message to return
    Params:
     - client (commands.client object) :
     - ctx (context object) : Used for sending msgs n stuff
     - Optional Params:
        - contentOne (string) : Embed title
        - contentTwo (string) : Embed description
        - timeout (int) : Timeout for wait_for
    Returns:
     - msg.content (string) : If a message is detected, the content will be returned
    or
     - False (bool) : If a timeout occurs
    """
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}",)
    sent = await ctx.send(embed=embed)
    try:
        msg = await client.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel,
        )
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False


class giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Giveaway Cog status: loaded')

    @commands.command(
        name="giveaway",
        description="Create a full giveaway!"
    )
    @commands.guild_only()
    async def giveaway(self, ctx):
        await ctx.send("Lets start this giveaway, answer the questions I ask and we shall proceed.")

        questionList = [
            ["What channel should it be in?", "Mention the channel"],
            ["How long should this giveaway last?", "`d|h|m|s`"],
            ["What are you giving away?", "I.E. Your soul hehe"]
        ]
        answers = {}

        for i, question in enumerate(questionList):
            answer = await GetMessage(self.client, ctx, question[0], question[1])

            if not answer:
                await ctx.send("You failed to answer, please answer quicker next time.")
                return

            answers[i] = answer

        embed = discord.Embed(name="Giveaway content")
        for key, value in answers.items():
            embed.add_field(name=f"Question: `{questionList[key][0]}`", value=f"Answer: `{value}`", inline=False)

        m = await ctx.send("Are these all valid?", embed=embed)
        await m.add_reaction("???")
        await m.add_reaction("????")

        try:
            reaction, member = await self.client.wait_for(
                "reaction_add",
                timeout=60,
                check=lambda reaction, user: user == ctx.author
                and reaction.message.channel == ctx.channel
            )
        except asyncio.TimeoutError:
            await ctx.send("Confirmation Failure. Please try again.")
            return

        if str(reaction.emoji) not in ["???", "????"] or str(reaction.emoji) == "????":
            await ctx.send("Cancelling giveaway!")
            return

        channelId = re.findall(r"[0-9]+", answers[0])[0]
        channel = self.client.get_channel(int(channelId))

        time = convert(answers[1])

        giveawayEmbed = discord.Embed(
            title="???? __**Giveaway**__ ????",
            description=answers[2]
        )
        giveawayEmbed.set_footer(text=f"This giveaway ends {time} seconds from this message.")
        giveawayMessage = await channel.send(embed=giveawayEmbed)
        await giveawayMessage.add_reaction("????")

        await asyncio.sleep(time)

        message = await channel.fetch_message(giveawayMessage.id)
        users = await message.reactions[0].users().flatten()
        users.pop(users.index(ctx.guild.me))
        users.pop(users.index(ctx.author))

        if len(users) == 0:
            await channel.send("No winner was decided")
            return

        winner = random.choice(users)

        await channel.send(f"**Congrats {winner.mention}!**\nPlease contact {ctx.author.mention} about your prize.")


def setup(client):
    client.add_cog(giveaway(client))