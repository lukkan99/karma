import os
import configparser
import shutil

from utils.logger import log

class Defaults:
    token = None
    dbots_token = None
    owner_id = None
    home = None
    command_prefix = "k!"
    praw_id = ""
    praw_secret = ""
    praw_agent = ""

class Config:
    def __init__(self):

        if not os.path.isfile("config/config.ini"):
            if not os.path.isfile("config/config.ini.example"):
                log.critical("There is no \"config.ini.example\" file in the \"config\" folder! Please go to the github repo and download it and then put it in the \"config\" folder!")
                os._exit(1)
            else:
                shutil.copy("config/config.ini.example", "config/config.ini")
                log.warning("Created the \"config.ini\" file in the config folder! Please edit the config and then run the bot again!")
                os._exit(1)

        self.config_file = "config/config.ini"

        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_file, encoding="utf-8")

        sections = {"Credentials", "Bot", "Reddit"}.difference(config.sections())
        if sections:
            log.critical("Could not load a section in the config file, please obtain a new config file from the github repo if regenerating the config doesn't work!")
            os._exit(1)
        self._token = config.get("Credentials", "Token", fallback=Defaults.token)
        self._dbots_token = config.get("Credentials", "Dbots_Token", fallback=Defaults.dbots_token)
        self.owner_id = config.get("Bot", "Owner_ID", fallback=Defaults.owner_id)
        self.home = config.get("Bot", "home", fallback=Defaults.owner_id)
        self.command_prefix = config.get("Bot", "Command_Prefix", fallback=Defaults.command_prefix)
        self.praw_id = config.get("Reddit", "PRAW_Client_ID", fallback=Defaults.praw_id)
        self.praw_secret = config.get("Reddit", "PRAW_Client_Secret", fallback=Defaults.praw_secret)
        self.praw_agent = config.get("Reddit", "PRAW_User_Agent", fallback=Defaults.praw_agent)


        self.check()

    def check(self):
        if not self._token:
            log.critical("No token was specified in the config, please put your bot's token in the config.")
            os._exit(1)

        if not self.owner_id:
            log.critical("No owner ID was specified in the config, please put your ID for the owner ID in the config")
            os._exit(1)

        if not self.home:
            log.critical("No home folder was specified in the config, please put your home folder in the config")
            os._exit(1)
