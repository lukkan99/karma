import discord
import requests
import praw
import random

from utils.config import Config
config = Config()

r = praw.Reddit(client_id=config.praw_id,
                     client_secret=config.praw_secret,
                     user_agent=config.praw_agent)

def get_avatar(user):
    if user.avatar:
        return user.avatar_url
    else:
        return user.default_avatar_url

def get_reddit(Subreddit, channel, forceimg=False):
    try:
        posts = list(r.subreddit(Subreddit).hot(limit=100))
    except:
        raise SearchError("What is that subreddit?!")

    def randomreddit():
        try:
            post = random.choice(posts)
        except:
            raise SearchError("Nothing found")
        if post.over_18 and channel != "nsfw" and not channel.startswith("nsfw-"):
            imgurl = "http://jaqreven.com/angery.png"
            pageurl = "https://en.wikipedia.org/wiki/Pornography_addiction"
            titletext = "Content rated 18+, please switch to an NSFW channel."
        else:
            imgurl = post.url
            pageurl = post.shortlink
            titletext = "/r/{}".format(Subreddit)

        foundit = False
        suffixes = [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".gif", ".tiff"]
        for suffix in suffixes:
            if suffix in imgurl:
                foundit = True
                break

        if foundit == True or forceimg == False:
            return imgurl, pageurl, titletext, foundit
        else:
            randomreddit()

    return randomreddit()

class SearchError(TypeError):
    """Eh nothing found, totally legit message"""
    pass
