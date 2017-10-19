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
from utils.lists import *
from utils.buildinfo import *
from time import strftime, gmtime

import platform
import itertools
import base64

import psutil


import discord
config = Config()

class Utils():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def support(self, ctx):
        """Get help related to the bot"""
        await self.bot.say("""Having a problem? You may either join our Discord or report an issue at our GitHub.
        GitHub: <https://github.com/jaqreven/karma/issues>
        Discord: <http://support.jaqreven.com>""")

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        """Get invite links for the bot"""
        await self.bot.say("Here's the link to invite me: <http://invite.jaqreven.com>")

    @commands.command(pass_context=True)
    async def b64(self, ctx, *, String:str):
        """Encode to / Decode from Base64"""
        try:
            string = String;
            encoded = base64.b64decode(string).decode('utf-8')
            try:
                await self.bot.say("**Decoded Base64 string:** {}".format(encoded.replace("@everyone", "@everyjuan").replace("@here", "@hare")))
            except:
                await self.bot.say("The message is too long!")
                return
        except:
            try:
                string = String.encode("utf-8");
                encoded = base64.b64encode(string)
                encoded = encoded.decode("utf-8");
                try:
                    await self.bot.say("**Encoded Base64 string:** {}".format(encoded))
                except:
                    await self.bot.say("The message is too long!")
                    return
            except:
                await self.bot.say("Invalid string.")


    @commands.command(pass_context=True)
    async def userinfo(self, ctx, *, Member:discord.Member=None):
        """Gets info about a user"""
        if Member == None:
            Member = ctx.message.author

        isbot = Member.bot
        Memberid = Member.id
        nick = Member.display_name
        name = Member.name

        joindate = "{}".format(str(Member.joined_at).split(".")[0].split(" ")[0])
        joindate = joindate.split("-")
        joindate = "{}.{}.{}".format(joindate[2], joindate[1], joindate[0])

        createdate = "{}".format(str(Member.created_at).split(".")[0].split(" ")[0])
        createdate = createdate.split("-")
        createdate = "{}.{}.{}".format(createdate[2], createdate[1], createdate[0])

        game = Member.game
        color = str(Member.colour).replace("0x", "#")
        status = str(Member.status).replace("dnd", "do not disturb")

        roles = ""
        for role in Member.roles:
            roles = "{}, {}".format(roles, role.name)
        roles = roles[2:]

        toprole = Member.top_role

        em = discord.Embed(description="\u200b")
        em.title = str(Member) + " - Info"
        em.set_thumbnail(url=get_avatar(Member))
        em.color = ctx.message.server.me.color

        em.add_field(name="Name", value=name, inline=True)
        em.add_field(name="Nick", value=nick, inline=True)
        em.add_field(name="ID", value=Memberid, inline=True)
        em.add_field(name="Is bot", value=isbot, inline=True)
        em.add_field(name="Server Join Date", value=joindate, inline=True)
        em.add_field(name="Account Creation Date", value=createdate, inline=True)
        em.add_field(name="Game", value=game, inline=True)
        em.add_field(name="Status", value=status, inline=True)
        em.add_field(name="Role Colour", value=color, inline=True)
        em.add_field(name="Highest role", value=toprole, inline=True)
        em.add_field(name="Roles", value=roles, inline=True)

        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
        await self.bot.send_message(ctx.message.channel, embed=em)


    @commands.command(pass_context=True)
    async def hide(self, ctx, channel:discord.Channel):
        """Hides (removes read perms) from a channel"""

        perms = channel.permissions_for(ctx.message.author)
        has_perms = perms.administrator
        if has_perms:
            raise PermissionsError("You have administrator permissions, I can't hide channels.")
            return

        if channel == ctx.message.server.default_channel:
            raise PermissionsError("It's not possible to hide the default channel.")
            return

        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = False

        try:
            await self.bot.edit_channel_permissions(channel, ctx.message.author, overwrite)
        except discord.errors.Forbidden:
            raise PermissionsError("The bot is missing permissions.")
            return

        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Channel Hiding"
        em.description = "Successfully hid the channel #{}. Use {}show to see it again.".format(channel.name, config.command_prefix)
        em.set_thumbnail(url=get_avatar(ctx.message.author))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    async def show(self, ctx, channel:discord.Channel):
        """Removes the read permissions override"""

        perms = channel.permissions_for(ctx.message.author)
        has_perms = perms.administrator
        if has_perms:
            raise PermissionsError("You have administrator permissions, I can't show channels.")
            return

        if channel == ctx.message.server.default_channel:
            raise PermissionsError("It's not possible to show the default channel, everyone can see it already..")
            return

        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = None

        try:
            if perms.send_messages:
                await self.bot.edit_channel_permissions(channel, ctx.message.author, overwrite)
            else:
                await self.bot.delete_channel_permissions(channel, ctx.message.author)
        except discord.errors.Forbidden:
            raise PermissionsError("The bot is missing permissions.")
            return

        em = discord.Embed(colour=ctx.message.server.me.color)
        em.title = "Channel Hiding"
        em.description = "Successfully showed the channel #{}. Use {}hide to hide it again.".format(channel.name, config.command_prefix)
        em.set_thumbnail(url=get_avatar(ctx.message.author))
        em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
        await self.bot.send_message(ctx.message.channel, embed=em)


class PermissionsError(TypeError):
    """User doesnt have permissions or something similar, I don't care"""


def setup(bot):
    bot.add_cog(Utils(bot))
