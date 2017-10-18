import discord
import requests


def get_avatar(user):
    if user.avatar:
        return user.avatar_url
    else:
        return user.default_avatar_url
