import asyncio
#import cat
import random
import os
import json
import urllib.request
import time
import sys

from utils.config import Config
from discord.ext import commands
from utils.tools import *
from time import strftime, gmtime


import psutil
import discord
config = Config()

class Moderation():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def ban(self, ctx, Member:discord.Member, *, reason:str="No reason specified"):
        """Bans someone. Supply a reason after member."""

        perms = ctx.message.channel.permissions_for(ctx.message.author)
        has_perms = perms.ban_members

        if not has_perms:
            raise PermissionsError("You don't have the permission `ban_members`")
            return
        if Member == ctx.message.author:
            raise PermissionsError("Eh.. what?!")
            return
        em = discord.Embed()
        em.title = "Bans"
        em.description = """You've been banned by **{}** from **{}**.
Reason: **{}**.""".format(ctx.message.author, ctx.message.server.name, reason)
        try:
            msg = await self.bot.send_message(Member, embed=em)
        except:
            pass
        try:
            await self.bot.ban(Member)
        except:
            em.description = """**{}** tried to ban you from **{}**.
Reason: **{}**.""".format(ctx.message.author, ctx.message.server.name, reason)
            try:
                await self.bot.edit_message(msg, embed=em)
            except:
                pass
            raise PermissionsError("The bot doesn't have permissions to ban the member **{}**".format(Member))
            return

        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Bans"
        em.description = """Successfully banned the member **{}**.
Command used by **{}**.
Reason: **{}**""".format(Member, ctx.message.author, reason)
        em.set_thumbnail(url=get_avatar(Member))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))

        await self.bot.send_message(ctx.message.channel, embed=em)



    @commands.command(pass_context=True)
    async def kick(self, ctx, Member:discord.Member, *, reason:str="No reason specified"):
        """Kicks someone. Supply a reason after member."""

        perms = ctx.message.channel.permissions_for(ctx.message.author)
        has_perms = perms.kick_members
        if not has_perms:
            raise PermissionsError("You don't have the permission `kick_members`")
            return
        if Member == ctx.message.author:
            raise PermissionsError("Eh.. what?!")
            return
        em = discord.Embed()
        em.title = "Kicks"
        em.description = """You've been kicked by **{}** from **{}**.
Reason: **{}**.""".format(ctx.message.author, ctx.message.server.name, reason)
        try:
            msg = await self.bot.send_message(Member, embed=em)
        except:
            pass
        try:
            await self.bot.kick(Member)
        except:
            em.description = """**{}** tried to kick you from **{}**.
Reason: **{}**.""".format(ctx.message.author, ctx.message.server.name, reason)
            try:
                await self.bot.edit_message(msg, embed=em)
            except:
                pass
            raise PermissionsError("The bot doesn't have permissions to kick the member **{}**".format(Member))
            return

        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Kicks"
        em.description = """Successfully kicked the member **{}**.
Command used by **{}**.
Reason: **{}**""".format(Member, ctx.message.author, reason)
        em.set_thumbnail(url=get_avatar(Member))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))

        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    async def mute(self, ctx, Member:discord.Member, *, channel:discord.Channel=None):
        """Mutes someone. Add a specific channel after member."""

        if channel:
            where = "in **#{}**".format(channel)
            channeli = channel
        else:
            where = "everywhere"
            channeli = ctx.message.channel

        perms = channeli.permissions_for(ctx.message.author)
        has_perms = perms.manage_messages
        if not has_perms:
            raise PermissionsError("You don't have the permission `manage_messages`")
            return

        if Member == self.bot.user:
            raise PermissionsError("Hey, don't mute me :(")
            return
        if Member == ctx.message.author:
            raise PermissionsError("Eh.. what?!")
            return

        perms = channeli.permissions_for(Member)
        has_perms = perms.administrator
        if has_perms:
            raise PermissionsError("**{}** has `administrator` permissions, I can't do this.".format(Member))
            return
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False

        try:
            await self.bot.edit_channel_permissions(channeli, Member, overwrite)
        except:
            raise PermissionsError("The bot doesn't have permissions to mute the member **{}**".format(Member))
            return
        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Mutes"
        em.description = """Successfully muted the member **{}** {}.
Command used by **{}**.""".format(Member, where, ctx.message.author)
        em.set_thumbnail(url=get_avatar(Member))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
        await self.bot.send_message(ctx.message.channel, embed=em)

        if not channel:
            for channel in ctx.message.server.channels:
                if not channel == ctx.message.channel:
                    await self.bot.edit_channel_permissions(channel, Member, overwrite)

    @commands.command(pass_context=True)
    async def unmute(self, ctx, Member:discord.Member, *, channel:discord.Channel=None):
        """Unmutes someone. Add a specific channel after member."""

        if channel:
            where = "in **#{}**".format(channel)
            channeli = channel
        else:
            where = "everywhere"
            channeli = ctx.message.channel


        perms = channeli.permissions_for(ctx.message.author)
        has_perms = perms.manage_messages
        if not has_perms:
            raise PermissionsError("You don't have the permission `manage_messages`")
            return

        if Member == self.bot.user:
            raise PermissionsError("Eh? :(")
            return
        if Member == ctx.message.author:
            raise PermissionsError("Eh.. what?!")
            return

        perms = channeli.permissions_for(Member)
        has_perms = perms.administrator
        if has_perms:
            raise PermissionsError("**{}** has `administrator` permissions, I can't do this.".format(Member))
            return
        if channel:
            where = "in **#{}**".format(channel)
            channeli = channel
        else:
            where = "everywhere"
            channeli = ctx.message.channel
        try:
            await self.bot.delete_channel_permissions(channeli, Member)
        except:
            raise PermissionsError("The bot doesn't have permissions to unmute the member **{}**".format(Member))
            return

        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Mutes"
        em.description = """Successfully unmuted the member **{}** {}.
Command used by **{}**.""".format(Member, where, ctx.message.author)
        em.set_thumbnail(url=get_avatar(Member))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
        await self.bot.send_message(ctx.message.channel, embed=em)

        if not channel:
            for channel in ctx.message.server.channels:
                if not channel == ctx.message.channel:
                    await self.bot.delete_channel_permissions(channel, Member)



    @commands.command(pass_context=True)
    async def purge(self, ctx, *, number:int):
        """Purges (mass deletes) messages."""

        perms = ctx.message.channel.permissions_for(ctx.message.author)
        has_perms = perms.manage_messages
        if not has_perms:
            raise PermissionsError("You don't have the permission `manage_messages`")
            return

        if number < 1:
            number = 1
        if number > 100:
            number = 100

        try:
            await self.bot.delete_message(ctx.message)
            deleted = await self.bot.purge_from(ctx.message.channel, limit=number)
        except:
            raise PermissionsError("The bot doesn't have permissions to delete the messages.")
            return

        if number == 1:
            deleted = "**{}** message".format(len(deleted))
        else:
            deleted = "**{}** messages".format(len(deleted))

        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Purge"
        em.description = """Successfully purged {}.
Command used by **{}**.""".format(deleted, ctx.message.author)
        em.set_thumbnail(url=get_avatar(ctx.message.author))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))

        msg = await self.bot.send_message(ctx.message.channel, embed=em)
        await asyncio.sleep(5)
        try:
            await self.bot.delete_message(msg)
        except:
            return
class PermissionsError(TypeError):
    """User doesnt have permissions or something similar, I don't care"""

def setup(bot):
    bot.add_cog(Moderation(bot))
