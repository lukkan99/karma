import asyncio
import random
import os
import json
import urllib.request
import time
import praw

from time import gmtime, strftime
from utils.config import Config
from discord.ext import commands
from utils.tools import *
from utils.lists import *

config = Config()

r = praw.Reddit(client_id=config.praw_id,
                     client_secret=config.praw_secret,
                     user_agent=config.praw_agent)

class Fun():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def say(self, ctx, *, Message:str):
        """I can like, say something. I'm so advanced."""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass
        await self.bot.say(u"\u200B" + Message.replace("@everyone", "@everyjuan").replace("@here", "@hare"))

    @commands.command(pass_context=True)
    async def pick(self, ctx, *, List:str):
        """I can pick from things seperated by commas (,)."""
        item = List.split(",")
        if len(item) < 2:
            raise SyntaxError("Give me multiple things to choose from seperated by commas.")
            return
        await self.bot.say("Hmm.. :thinking:.. I'd choose {}".format(random.choice(item)).replace("  ", " ").replace("@everyone", "@everyjuan").replace("@here", "@hare"))


    @commands.command(pass_context=True)
    async def reverse(self, ctx, *, Message:str):
        """The thing you told me, but.. backwards."""
        await self.bot.say(u"\u200B" + Message[::-1].replace("@everyone", "@everyjuan").replace("@here", "@hare"))

    @commands.command(pass_context=True)
    async def mocking(self, ctx, *, Message:str):
        """WhY dId YoU dO tHiS"""
        ret = ""
        i = True  # capitalize
        for char in Message:
            if i:
                ret += char.upper()
            else:
                ret += char.lower()
            if char != ' ':
                i = not i
        location = config.home + "pics/mocking.jpg"
        await self.bot.send_file(ctx.message.channel, location, content=ret.replace("@everyone", "@everyjuan").replace("@here", "@hare"))



    @commands.command(pass_context=True)
    async def insult(self, ctx, *, Member:discord.Member):
        """Insult someone, lol!"""

        randinsult = random.choice(open(config.home + "txt/insult.txt", encoding='utf-8').readlines()).rstrip('\n')
        randinsult = randinsult.format(Member.display_name, ctx.message.author.display_name)
        if Member.id == "152078083522822145":
            randinsult = "Okay, how would I insult you.. uhh.. YOU'RE SUPER CUTE AND I LOVE YOU! Yeah, that works."
        await self.bot.say(randinsult + ".")

    @commands.command(pass_context=True)
    async def ship(self, ctx, Member:discord.Member, Member2:discord.Member=None):
        """It's like asking someone out, but it looks like a joke."""

        if Member2 == None:
            Member2 = ctx.message.author

        if Member == Member2:
            await self.bot.say("What's this, selfcest?")
            return

        good = random.choice(shipcomments)


        Member2i = int(str(Member2.id)[:-1])
        memberi = int(str(Member.id)[:-1])
        if Member2i > memberi:
            p1, p2 = Member2.display_name, Member.display_name
        else:
            p1, p2 = Member.display_name, Member2.display_name

        div1, div2 = (len(p1) + 1) // 2, (len(p2) - 1) // 2
        p1, p2 = p1[:div1], p2[div2:]
        shipname = p1 + p2

        msg = "{}\n**{}** + **{}** = **{}**.".format(good, Member.display_name, Member2.display_name, shipname)

        await self.bot.say(msg)







    #
    #▒█▀▀▀█ ▒█░▒█ ▀█▀ ▀▀█▀▀ ▒█▀▀█ ▒█▀▀▀█ ▒█▀▀▀█ ▀▀█▀▀
    #░▀▀▀▄▄ ▒█▀▀█ ▒█░ ░▒█░░ ▒█▄▄█ ▒█░░▒█ ░▀▀▀▄▄ ░▒█░░
    #▒█▄▄▄█ ▒█░▒█ ▄█▄ ░▒█░░ ▒█░░░ ▒█▄▄▄█ ▒█▄▄▄█ ░▒█░░
    #

    @commands.command()
    async def one(self):
        """Haha, we are number one, lol"""

        chars = random.choice(open(config.home + "txt/characters.txt", encoding='utf-8').readlines()).rstrip('\n')
        vid = random.choice(open(config.home + "txt/one.txt").readlines())
        await self.bot.say("{} gave you a #1 meme: {}".format(chars, vid))


    @commands.command()
    async def horror(self):
        """Creepy kids videos (minions etc)"""

        chars = random.choice(open(config.home + "txt/characters.txt", encoding='utf-8').readlines()).rstrip('\n')
        vid = random.choice(open(config.home + "txt/horror.txt").readlines())
        await self.bot.say("Eh, I'm blaming {} for this one: {}".format(chars, vid))

    @commands.command()
    async def intro(self):
        """broken for now"""

        chars = random.choice(open(config.home + "txt/characters.txt", encoding='utf-8').readlines()).rstrip('\n')
        vid = random.choice(open(config.home + "txt/intros.txt").readlines())
        await self.bot.say("Eh, I'm blaming {} for this one: {}".format(chars, vid))


    @commands.command(pass_context=True)
    async def meme(self, ctx):
        """Random image shitpost"""

        msg = await self.bot.say("Searching for a dank meme..")

        imgurl, pageurl, titletext, foundit = get_reddit("dankmemes", ctx.message.channel.name, True)

        em = discord.Embed()
        if foundit == True:
            em.set_image(url=imgurl)
        else:
            em.description = imgurl

        em.url = pageurl
        em.title = titletext
        em.color = ctx.message.server.me.color
        em.set_footer(text="{}".format(ctx.message.author))
        await self.bot.edit_message(msg, "​", embed=em)


    @commands.command(pass_context=True)
    async def rulettaja(self, ctx):
        """Leaked pics of a Finnish Youtuber"""
        location = config.home + "pics/rulettaja/" + random.choice(os.listdir(config.home + "pics/rulettaja"))
        msg = random.choice(dabtype)
        await self.bot.send_file(ctx.message.channel, location, content=msg)


    @commands.command(pass_context=True)
    async def surreal(self, ctx):
        """Let's pretend that surreal memes aren't dead yet."""

        msg = await self.bot.say("Searching for a surreal meme..")

        imgurl, pageurl, titletext, foundit = get_reddit("surrealmemes", ctx.message.channel.name, True)

        em = discord.Embed()
        if foundit == True:
            em.set_image(url=imgurl)
        else:
            em.description = imgurl

        em.url = pageurl
        em.title = titletext
        em.color = ctx.message.server.me.color
        em.set_footer(text="{}".format(ctx.message.author))
        await self.bot.edit_message(msg, "​", embed=em)


    @commands.command(pass_context=True)
    async def dab(self, ctx):
        """Haha, it's still 2015, right?"""

        chars = random.choice(open(config.home + "txt/characters.txt", encoding='utf-8').readlines()).rstrip('\n')
        chars = "**{}** is dabbing.. {} I blame {} for this..".format(ctx.message.author.display_name, random.choice(dabtype), chars)
        meme = config.home + "pics/dab/" + random.choice(os.listdir(config.home + "pics/dab"))
        await self.bot.send_file(ctx.message.channel, meme, content=chars)



    @commands.command(pass_context=True)
    async def drink(self, ctx, Member:discord.Member=None):
        """Why sipp or succ when you can drincc"""

        if Member == None:
            Member = ctx.message.author

        drink = random.choice(os.listdir(config.home + "pics/drink"))
        name = drink.split(".")[0]
        location = config.home + "pics/drink/" + drink

        msg = "**{}** drank some **{}**.".format(Member.display_name, name)
        await self.bot.send_file(ctx.message.channel, location, content=msg)

    #
    # ▒█▀▀█ ░█▀▀█ ▒█▀▄▀█ ▒█▀▀▀ ▒█▀▀▀█
    # ▒█░▄▄ ▒█▄▄█ ▒█▒█▒█ ▒█▀▀▀ ░▀▀▀▄▄
    # ▒█▄▄█ ▒█░▒█ ▒█░░▒█ ▒█▄▄▄ ▒█▄▄▄█
    #


    @commands.command(pass_context=True)
    async def typerace(self, ctx):
        """Starts a typerace"""

        if random.randint(0, 1) == 1:
            objekti2 = random.choice(objekti) + " " + random.choice(adverbi)
        else:
            objekti2 = random.choice(objekti)
        typethis = "{} {} {}.".format(
        random.choice(subjekti),
        random.choice(predikaatti),
        objekti2)

        times = 5
        timer = times
        msg = await self.bot.say("**{}'s typerace >** Typerace starts in **{}**s! Get ready to type in all lower case. Don't forget the dot.".format(ctx.message.author.display_name, timer))
        for i in range(times):
            timer = times - i
            await self.bot.edit_message(msg, "**{}'s typerace >** Typerace starts in **{}**s! Get ready to type in all lower case. Don't forget the dot.".format(ctx.message.author.display_name, timer))
            await asyncio.sleep(1)

        time1 = time.time()
        await self.bot.edit_message(msg, "**{0}'s typerace >** Typerace started! The first to type ```{1}``` in all lower case wins. Don't forget the dot. 60 seconds timeout.".format(ctx.message.author.display_name, typethis.upper()))
        response = await self.bot.wait_for_message(content=str(typethis).lower(), channel=ctx.message.channel, timeout=60)

        if response == None:
            await self.bot.edit_message(msg, "**{}'s typerace >** :skull_crossbones: You were too slow! :skull_crossbones:".format(ctx.message.author.display_name))
            await self.bot.say("**{}'s typerace >** :skull_crossbones: You were too slow! :skull_crossbones:".format(ctx.message.author.display_name))
        else:
            time2 = time.time()
            time3 = time2 - time1
            time3 = round(time3, 3)
            await self.bot.edit_message(msg, """**{0}'s typerace >** Typerace started! The first to type ```{1}``` in all lower case wins. Don't forget the dot. 60 seconds timeout.
```css\nTyperace is over and {2} won.```""".format(ctx.message.author.display_name, typethis.upper(), response.author.display_name))
            await self.bot.say("**{}'s typerace >** :trophy: **{}** won the typerace in **{}s**! Congratulations! :trophy:".format(ctx.message.author.display_name, response.author.display_name, time3))
        return
class ChannelError(TypeError):
    """Eh wrong channel, totally legit message"""
    pass
class SearchError(TypeError):
    """Eh nothing found, totally legit message"""
    pass
def setup(bot):
    bot.add_cog(Fun(bot))
