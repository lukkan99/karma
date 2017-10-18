import asyncio
import random
import os
import json
import urllib.request
import time

from utils.config import Config
from discord.ext import commands
from utils.tools import *
from utils.lists import *


config = Config()

class Roleplay():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def fucl(self, ctx, *, Member:discord.Member=""):
        """wait you arent supposed to see this"""
        if Member == "":
            Member = ctx.message.author
        raise TypeError("<@{}> not found in straight()".format(Member.id))


    @commands.command(pass_context=True)
    async def hug(self, ctx, Member:discord.Member):
        """Give your friend a nice, friendly hug!"""

        if Member.id == ctx.message.author.id:
            await self.bot.say("Are you so lonely that you have to hug yourself? Aww, that is so sad.. *hugs*")
            return

        loc = config.home + "pics/hug/" + random.choice(os.listdir(config.home + "pics/hug"))
        msg = "**{}** is hugging **{}**".format(ctx.message.author.display_name, Member.display_name)
        await self.bot.send_file(ctx.message.channel, loc, content=msg)

    @commands.command(pass_context=True)
    async def succ(self, ctx, Member:discord.Member):
        """Succ's not dead, right? [NSFW channel required]"""
        if not ctx.message.channel.name == "nsfw" and not ctx.message.channel.name.startswith("nsfw-"):
            raise ChannelError("The channel isn't named `nsfw` or the name doesn't start with `nsfw-`.")
            return

        if Member.id == ctx.message.author.id:
            await self.bot.say("Autofellation huh? Sorry, but you are in the majority that isn't able to do it.")
            return

        loc = config.home + "pics/succ/" + random.choice(os.listdir(config.home + "pics/succ"))
        msg = "**{}** is succing **{}**".format(ctx.message.author.display_name, Member.display_name)
        await self.bot.send_file(ctx.message.channel, loc, content=msg)

    @commands.command(pass_context=True)
    async def ahn(self, ctx, Member:discord.Member):
        """ahn"""
        if Member.id == ctx.message.author.id:
            await self.bot.say("Auto<:ahn:361606131463880704> huh? Sorry, but you are in the majority that isn't able to do it.")
            return

        em = discord.Embed()
        em.set_image(url="https://i.imgur.com/IDOe2pi.png")
        em.color = ctx.message.server.me.color
        em.title = "**{}** is <:ahn:361606131463880704>ing **{}**".format(ctx.message.author.display_name, Member.display_name)
        await self.bot.send_message(ctx.message.channel, embed=em)


    @commands.command(pass_context=True)
    async def kiss(self, ctx, Member:discord.Member):
        """Kisses are pretty neat. Too bad no one ever kisses me."""

        if Member.id == ctx.message.author.id:
            await self.bot.say("How would you even kiss yourself? Like you'd kiss your hand or shit? ew..")
            return

        loc = config.home + "pics/kiss/" + random.choice(os.listdir(config.home + "pics/kiss"))
        msg = "**{}** is kissing **{}**".format(ctx.message.author.display_name, Member.display_name)
        await self.bot.send_file(ctx.message.channel, loc, content=msg)


    @commands.command(pass_context=True)
    async def pat(self, ctx, Member:discord.Member):
        """Patting.. like you know. That's pretty adorable."""

        if Member.id == ctx.message.author.id:
            await self.bot.say("Why would you do that? Are you really so lonely?")
            return

        loc = config.home + "pics/pat/" + random.choice(os.listdir(config.home + "pics/pat"))
        msg = "**{}** is patting **{}**".format(ctx.message.author.display_name, Member.display_name)
        await self.bot.send_file(ctx.message.channel, loc, content=msg)

class ChannelError(TypeError):
    """Eh wrong channel, totally legit message"""
    pass

def setup(bot):
    bot.add_cog(Roleplay(bot))
