import asyncio
import random
import json
import urllib.request
from discord.ext import commands

from utils.tools import *
from utils.lists import *

from utils.config import Config
config = Config()



class Pics():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def reddit(self, ctx, *, Subreddit:str):
        """Gets a reddit pic. [NSFW/SFW, DEPENDS ON THE CHANNEL]"""
        msg = await self.bot.say("Searching for a post in /r/{}...".format(Subreddit))

        imgurl, pageurl, titletext, foundit = get_reddit(Subreddit, ctx.message.channel.name, False)

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
    async def pokemon(self, ctx, *, Pokemon):
        """Pick any Pokemon and get a random picture. [SFW]"""
        if Pokemon.lower() in (name.lower() for name in pokemons):

            msg = await self.bot.say("Searching for a cool {}...".format(Pokemon.title()))

            tag = "{} score:>=3 order:random".format(Pokemon.replace(" ", "_"))
            data = json.loads(requests.get("https://e926.net/post/index.json?limit=99&tags={}".format(tag)).text)

            for i in range(99):
                try:
                    imgdata = data[i-1]
                except:
                    raise SearchError("Woops, that Pokemon isn't popular enough on e926. :(")
                blacklist = False

                if len(imgdata["tags"]) > 350:
                    blacklist = True
                for blacklisted in pokeblacklist:
                    if blacklisted in imgdata["tags"]:
                        blacklist = True

                if blacklist == False:
                    break

            em = discord.Embed()
            em.set_image(url=imgdata["file_url"])
            em.color = ctx.message.server.me.color
            em.set_footer(text="E926 | {} | {}".format(Pokemon.title(), ctx.message.author))
            await self.bot.edit_message(msg, "​", embed=em)
        else:
            raise SearchError("That's not a valid Pokemon!")

    @commands.command(pass_context=True)
    async def shibe(self, ctx):
        """Gets shibe images from shibe.online [SFW]"""
        await self.bot.send_typing(ctx.message.channel)

        url = json.loads(requests.get("http://shibe.online/api/shibes?count=1").text)[0]

        em = discord.Embed()
        em.set_footer(text="Shibe.online | {}".format(ctx.message.author))
        em.color = ctx.message.server.me.color
        em.set_image(url=url)
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    async def e926(self, ctx, *, tags:str):
        """Gets e926 images [SFW]"""
        await self.bot.send_typing(ctx.message.channel)

        try:
            data = json.loads(requests.get("https://e926.net/post/index.json?limit=1&tags={} order:random".format(tags)).text)
        except json.JSONDecodeError:
            raise SearchError("No results found for `{}`".format(tags))
            return
        count = len(data)

        if count == 0:
            raise SearchError("No results found for `{}`".format(tags))
            return

        imgdata = data[0]
        imgurl = imgdata["file_url"]
        score = imgdata["score"]
        dimensions = str(imgdata["width"]) + "x" + str(imgdata["height"])
        rating = imgdata["rating"]
        artist = ", ".join(imgdata["artist"])
        source = "https://e926.net/post/show/{}".format(imgdata["id"])

        em = discord.Embed()
        if ctx.message.author.avatar:
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url
        em.url = source
        em.title = tags
        em.description = """**Score**: {} | **Resolution**: {} | **Rating**: {}
**Author(s)**: {}""".format(score, dimensions, rating, artist)
        em.set_footer(text="E926 | {}".format(ctx.message.author))
        em.color = ctx.message.server.me.color
        em.set_image(url=imgurl)
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    async def sb(self, ctx, *, tags:str):
        """Gets Safebooru images [SFW]"""

        await self.bot.send_typing(ctx.message.channel)

        try:
            data = json.loads(requests.get("https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&limit=1000&tags={}".format(tags)).text)
        except json.JSONDecodeError:
            raise SearchError("No results found for `{}`".format(tags))
            return
        count = len(data)

        if count == 0:
            raise SearchError("No results found for `{}`".format(tags))
            return

        imgdata = data[0]
        imgurl = "https://safebooru.org/images/{}/{}".format(imgdata["directory"], imgdata["image"])
        score = imgdata["score"]
        dimensions = str(imgdata["width"]) + "x" + str(imgdata["height"])
        rating = imgdata["rating"]
        source = "https://safebooru.org/index.php?page=post&s=view&id={}".format(imgdata["id"])

        em = discord.Embed()
        if ctx.message.author.avatar:
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url
        em.url = source
        em.title = tags
        em.description = "**Score**: {} | **Resolution**: {} | **Rating**: {}".format(score, dimensions, rating)
        em.set_footer(text="Safebooru | {}".format(ctx.message.author))
        em.color = ctx.message.server.me.color
        em.set_image(url=imgurl)
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    async def e621(self, ctx, *, tags:str):
        """Gets e621 images [NSFW]"""
        if not ctx.message.channel.name == "nsfw" and not ctx.message.channel.name.startswith("nsfw-"):
            raise ChannelError("The channel isn't named `nsfw` or the name doesn't start with `nsfw-`.")
            return
        await self.bot.send_typing(ctx.message.channel)

        try:
            data = json.loads(requests.get("https://e621.net/post/index.json?limit=1&tags={} order:random".format(tags)).text)
        except json.JSONDecodeError:
            raise SearchError("No results found for `{}`".format(tags))
            return
        count = len(data)

        if count == 0:
            raise SearchError("No results found for `{}`".format(tags))
            return
        imgdata = data[0]
        imgurl = imgdata["file_url"]
        score = imgdata["score"]
        dimensions = str(imgdata["width"]) + "x" + str(imgdata["height"])
        rating = imgdata["rating"]
        artist = ", ".join(imgdata["artist"])
        source = "https://e621.net/post/show/{}".format(imgdata["id"])

        em = discord.Embed()
        if ctx.message.author.avatar:
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url
        em.url = source
        em.title = tags
        em.description = """**Score**: {} | **Resolution**: {} | **Rating**: {}
**Author(s)**: {}""".format(score, dimensions, rating, artist)
        em.set_footer(text="E621 | {}".format(ctx.message.author))
        em.color = ctx.message.server.me.color
        em.set_image(url=imgurl)
        await self.bot.send_message(ctx.message.channel, embed=em)


    @commands.command(pass_context=True)
    async def r34(self, ctx, *, tags:str):
        """Gets Rule34 images [NSFW]"""
        if not ctx.message.channel.name == "nsfw" and not ctx.message.channel.name.startswith("nsfw-"):
            raise ChannelError("The channel isn't named `nsfw` or the name doesn't start with `nsfw-`.")
            return
        await self.bot.send_typing(ctx.message.channel)

        try:
            data = json.loads(requests.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit=1000&tags={}".format(tags)).text)
        except json.JSONDecodeError:
            raise SearchError("No results found for `{}`".format(tags))
            return
        count = len(data)

        if count == 0:
            raise SearchError("No results found for `{}`".format(tags))
            return

        imgdata = data[0]
        imgurl = "http://img.rule34.xxx/images/{}/{}".format(imgdata["directory"], imgdata["image"])
        score = imgdata["score"]
        dimensions = str(imgdata["width"]) + "x" + str(imgdata["height"])
        rating = imgdata["rating"]
        source = "http://rule34.xxx/index.php?page=post&s=view&id={}".format(imgdata["id"])

        em = discord.Embed()
        if ctx.message.author.avatar:
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url
        em.url = source
        em.title = tags
        em.description = "**Score**: {} | **Resolution**: {} | **Rating**: {}".format(score, dimensions, rating)
        em.set_footer(text="Rule34 | {}".format(ctx.message.author))
        em.color = ctx.message.server.me.color
        em.set_image(url=imgurl)
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    async def gb(self, ctx, *, tags:str):
        """Gets Gelbooru images [NSFW]"""
        if not ctx.message.channel.name == "nsfw" and not ctx.message.channel.name.startswith("nsfw-"):
            raise ChannelError("The channel isn't named `nsfw` or the name doesn't start with `nsfw-`.")
            return
        await self.bot.send_typing(ctx.message.channel)

        try:
            data = json.loads(requests.get("https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=1000&tags={}".format(tags)).text)
        except json.JSONDecodeError:
            raise SearchError("No results found for `{}`".format(tags))
            return
        count = len(data)

        if count == 0:
            raise SearchError("No results found for `{}`".format(tags))
            return

        imgdata = data[0]
        imgurl = "https://assets.gelbooru.com/images/{}/{}".format(imgdata["directory"], imgdata["image"]).replace("\/", "/")
        score = imgdata["score"]
        dimensions = str(imgdata["width"]) + "x" + str(imgdata["height"])
        rating = imgdata["rating"]
        source = "https://gelbooru.com/index.php?page=post&s=view&id={}".format(imgdata["id"])

        em = discord.Embed()
        if ctx.message.author.avatar:
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url
        em.url = source
        em.title = tags
        em.description = "**Score**: {} | **Resolution**: {} | **Rating**: {}".format(score, dimensions, rating)
        em.set_footer(text="Gelbooru | {}".format(ctx.message.author))
        em.color = ctx.message.server.me.color
        em.set_image(url=imgurl)
        await self.bot.send_message(ctx.message.channel, embed=em)


class ChannelError(TypeError):
    """Eh wrong channel, totally legit message"""
    pass
class SearchError(TypeError):
    """Eh nothing found, totally legit message"""
    pass


def setup(bot):
    bot.add_cog(Pics(bot))
