import os
import asyncio
import aiohttp
import sys
import time
import subprocess
import psutil
import random
import platform

from time import gmtime, strftime

from discord.ext import commands
from utils.config import Config
from utils.tools import *

from utils.shards import shard_count
from utils.logger import log

import builtins
from utils.buildinfo import *
import argparse

start_time = time.time()

log.init() # Yes I could just use __init__ but I'm dumb


cmdcount = 0

parser = argparse.ArgumentParser()
parser.add_argument("shard_id", help="Gets your shard ID. Shards enabled: {}".format(shard_count), type=int)
args = parser.parse_args()

# PLEASE FOR THE LOVE OF JESUS SOMEONE FIGURE OUT A BETTER SYSTEM
# LIKE A THING THAT STARTS ALL SHARDS AUTOMATICALLY

shard_id = args.shard_id

config = Config()
log.enableDebugging() # hi this is totally my original code *cough*
bot = commands.Bot(command_prefix=config.command_prefix, description="A bot for shitposting, NSFW, moderation etc.", shard_id=shard_id, shard_count=shard_count)
aiosession = aiohttp.ClientSession(loop=bot.loop)


async def set_default_status():
    type = discord.Status.online
    game = discord.Game(name="{0}help | Shard {1}/{2} | {3} servers on shard {1}".format(str(config.command_prefix), shard_id + 1, shard_count, len(bot.servers)))
    await bot.change_presence(status=type, game=game)

async def bot_shutdown():
    try:
        aiosession.close()
    except:
        pass
    await bot.logout()

@bot.event
async def on_server_join(server):

    await set_default_status()


@bot.event
async def on_server_remove(server):
    await set_default_status()

@bot.event
async def on_ready():
    codename = BUILD_CODENAME.split("<")[0].replace("*", "")
    print("\n")
    print("Logged in.\n\nUser: {}\nUser ID: {}\nShard: {}".format(bot.user, bot.user.id, shard_id))
    print("Version: {}\nAuthor: {}\nCodename: {}\nBuild date: {}\n".format(BUILD_VERSION, BUILD_AUTHORS, codename, BUILD_DATE))
    log.debug("Debugging is enabled!\n\n")
    await set_default_status()
    for extension in os.listdir("commands"):
            if extension.endswith(".py"):
                try:
                    bot.load_extension("commands." + extension[:-3])
                    log.debug("Loaded extension {}.".format(extension))
                except Exception as e:
                    log.error("Error in extension {}\n{}: {}".format(extension, type(e).__name__, e))
    if config._dbots_token:
        print("\n")
        log.debug("Updating DBots Statistics...")
        r = requests.post("https://bots.discord.pw/api/bots/{}/stats".format(bot.user.id), json={"shard_id": shard_id, "shard_count": shard_count, "server_count":len(bot.servers)}, headers={"Authorization":config._dbots_token})
        if r.status_code == 200:
            log.info("Discord Bots Server count updated.")
        elif r.status_code == 401:
            log.error("Woah, unauthorized?")
        else:
            log.error("An unknown error occured..")
    print("\nReady!\n\n")


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, discord.Forbidden) or isinstance(error, discord.NotFound):
        return

    em = discord.Embed(colour=ctx.message.server.me.color)
    em.set_author(name=random.choice(errormsgs), icon_url=ctx.message.author.avatar_url)
    em.description = str(error)
    em.set_footer(text="{0}support | {1}".format(config.command_prefix, ctx.message.author))

    try:
        await bot.send_message(ctx.message.channel, embed=em)
    except:
        return
    e = str(error).encode('ascii', 'replace')
    log.error("An error occured while executing command {}: {}".format(ctx.command.qualified_name, e))

@bot.event
async def on_command(command, ctx):
    log.info("[Serv {}] [User {}]: {}".format(ctx.message.server.id, ctx.message.author.id, ctx.message.content.split(" ")[0]))

    global cmdcount
    cmdcount = cmdcount + 1


@bot.event
async def on_message(message):

    if message.author.bot or message.channel.is_private:
        return

    message.content = message.content.replace("@everyone", "@everyjuan").replace("@here", "@hare")
    await bot.process_commands(message)


@bot.command(pass_context=True, hidden=True)
async def shutdown(ctx):
    """Turns the bot off"""
    if ctx.message.author.id == config.owner_id:
        await bot.say("Bye!")
        log.warning("{} has turned off the bot!".format(ctx.message.author))
        await bot_shutdown()

@bot.command(pass_context=True)
async def stats(ctx):
    """Gets various stats about the bot"""
    members = sum(len(s.members) for s in bot.servers) * int(shard_count)
    online = int(sum(1 for m in bot.get_all_members() if m.status != discord.Status.offline)) * int(shard_count)
    servers = int(len(bot.servers)) * int(shard_count)
    channels = int(sum(len(s.channels) for s in bot.servers)) * int(shard_count)


    cpuse = psutil.cpu_percent()
    cpucore = psutil.cpu_count(logical=False)
    cputhread = psutil.cpu_count(logical=True)

    pyver = str(sys.version).split(" ")[0]
    discpy = str(discord.__version__)
    centver = str(platform.release()).split("-")[0]

    mem = psutil.virtual_memory()
    memt = str(mem.total / 1024 / 1024).split(".")[0]
    mema = str(mem.available / 1024 / 1024).split(".")[0]
    memu = str(mem.used / 1024 / 1024).split(".")[0]


    s2 = time.time()

    total_seconds = s2 - start_time
    # Helper vars:
    MINUTE  = 60
    HOUR = MINUTE * 60
    DAY    = HOUR * 24

    # Get the days, hours, etc:
    days = int( total_seconds / DAY )
    hours = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )

    total_minutes = total_seconds / 60

    acmdcount = cmdcount + 1
    newcmds = acmdcount / total_minutes
    newcmds = round(newcmds, 3)

    uptime = ""
    if days > 0:
        uptime += str(days) + "" + (days == 1 and " day" or " days" ) + ",\n"
    if len(uptime) > 0 or hours > 0:
        uptime += str(hours) + "" + (hours == 1 and " hour" or " hours" ) + ",\n"
    if len(uptime) > 0 or minutes > 0:
        uptime += str(minutes) + "" + (minutes == 1 and " minute" or " minutes" ) + ",\n"
    uptime += str(seconds) + "" + (seconds == 1 and " second" or " seconds" )

    developer = int(config.owner_id)
    developer = await bot.get_user_info(developer)

    em = discord.Embed(description="\u200b")
    em.title = bot.user.name + " Stats"
    em.set_thumbnail(url=bot.user.avatar_url)
    em.color = ctx.message.server.me.color

    em.add_field(name="Developer", value=":bust_in_silhouette: {}".format(developer), inline=True)
    em.add_field(name='Commands', value=":arrow_forward: Commands: {}\n:arrows_counterclockwise: Cmds/min: {}".format(acmdcount, newcmds), inline=True)

    em.add_field(name='Members', value="<:offline:313956277237710868> Total: {}\n<:online:313956277808005120> Online: {}".format(members, online), inline=True)
    em.add_field(name='CPU', value=":heavy_division_sign: Usage: {}%\n:heavy_multiplication_x: Cores: {}c/{}t".format(cpuse, cpucore, cputhread), inline=True)
    em.add_field(name='Uptime', value=":alarm_clock: " + uptime.replace("\n", "\n:alarm_clock: "), inline=True)
    em.add_field(name='Bot', value=":desktop: Servers: {}\n:slot_machine: Channels: {}\n:diamond_shape_with_a_dot_inside: Shard: {}/{}".format(servers, channels, shard_id+1, shard_count), inline=True)

    em.add_field(name="Versions", value="<:python:326138379689525259> Python {}\n<:discord:314003252830011395> discord.py {}\n<:centos:326138388576993301> CentOS {}".format(pyver, discpy, centver), inline=True)
    em.add_field(name="Memory", value=":film_frames: Total: {}mb\n:film_frames: Available: {}mb\n:film_frames: Used: {}mb".format(memt, mema, memu), inline=True)
    em.add_field(name=bot.user.name, value="Version: {}\nCodename: {}\nDate: {}".format(BUILD_VERSION, BUILD_CODENAME, BUILD_DATE), inline=True)

    em.set_footer(text=strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
    await bot.send_message(ctx.message.channel, embed=em)

bot.run(config._token)
