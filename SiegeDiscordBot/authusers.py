import csv
import requests
import discord.embeds
import logging

import parts.dicts as dicts

class User:
    all = []
    __dIDs = []
    def __init__(self, siege_name, dID = 0, siege_ID = 0, rank = None):
        self.__siege_name = siege_name
        self.__dID        = dID
        self.__siege_ID   = siege_ID
        self.__rank       = rank

        if dID != 0:
            User.all.append(self)
            User.__dIDs.append(dID)

    @property 
    def siege_name(self):
        return self.__siege_name

    @property 
    def dID(self):
        return self.__dID

    @property 
    def siege_ID(self):
        return self.__siege_ID

    @property 
    def rank(self):
        return self.__rank

    @classmethod
    def instantiate_from_csv(cls):
        """
        --- Loading all authorized users from csv
        """
        User.all.clear()
        logging.info('Instantiating from csv')
        try:
            with open("./SiegeDiscordBot/db/stats.csv", 'r') as f:
                reader = csv.DictReader(f)
                items = list(reader)
                logging.info('./SiegeDiscordBot/db/stats.csv loaded')

            for item in items:
                User(
                    siege_name = item.get('siege_name'),
                    siege_ID   = item.get('siege_ID'),
                    dID        = int(item.get('dID')),
                    rank       = item.get('rank')
                )
            logging.info('Users loaded')
        except FileNotFoundError:
            logging.exception("No such file or directory: './db/stats.csv'")
            raise FileNotFoundError("[Errno 2] No such file or directory: './db/stats.csv'")
    
    @staticmethod
    def save_instance_to_csv():
        """
        --- Saving all authorized users to csv
        """
        logging.info('Saving instance to csv')
        header = ['siege_name', 'siege_ID', 'dID', 'rank']
        with open("./SiegeDiscordBot/db/stats.csv", 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            users_data = []
            logging.info('Creating data')
            for user in User.all:
                user_data = {
                    "siege_name": user.__siege_name,
                    "siege_ID": user.__siege_ID,
                    "dID": user.__dID,
                    "rank": user.__rank
                }
                users_data.append(user_data)
            logging.info('Writing data')
            writer.writeheader()
            writer.writerows(users_data)
        logging.info('All userdata saved')

    @staticmethod
    def get_by_dID(dID):
        """
        --- Getting user by his discord ID
        """
        try:
            ind = User.__dIDs.index(dID)
            logging.info(f"Found a user by dID: {dID}")
            return User.all[ind]
        except ValueError: # Catching ValueError if User is not authorized
            logging.exception("User is not authorized")
            return None

    @staticmethod
    def is_authorized(dID) -> bool:
        """
        --- Checking if user is authorized
        """
        try:
            ind = User.__dIDs.index(dID)
            logging.warning(f"User already authorized: {dID}")
            return True
        except ValueError: # Catching ValueError if User is not authorized
            logging.info("User is not authorized")
            return False

    @staticmethod
    def delete_by_dID(dID):
        try:
            ind = User.__dIDs.index(dID)
            User.all.pop(ind)
            User.__dIDs.pop(ind)
            logging.info(f"Deleted a user by dID: {dID}")
        except ValueError: # Catching ValueError if User is not authorized
            logging.exception("User is not authorized")    

    def __unpack_stats(self, r):
        """
        --- Getting stats from response
        """
        stats = {}
        logging.info(f"Unpacking raw stats")
        raw = r.json()[0]

        stats["title"]         = 'Tabstats'
        stats["siege_ID"]      = raw.get('profile').get('user_id')
        stats["url"]           = f"https://tabstats.com/siege/player/{self.__siege_name}/{stats.get('siege_ID')}"
        stats["avatar_url"]    = f'https://ubisoft-avatars.akamaized.net/{stats.get("siege_ID")}/default_146_146.png'
        csrr = raw.get('current_season_ranked_record')
        if not csrr:
            stats["full_rank"] = "No matches played this season"
            stats["rank"]      = "No matches played this season"
            stats["rank_url"]  = dicts.ranks_pics.get("No matches played this season")
        else:
            stats["rank"]           = csrr.get('rank_slug')[3:].split('-')[0]
            stats["rank_url"]       = dicts.ranks_pics.get(stats.get("rank"))
            stats["full_rank"]      = csrr.get('rank_slug')[3:].replace('-', ' ')

            stats["mmr"]            = csrr.get('mmr')
            stats["mmr_change"]     = csrr.get('mmr_change')

            stats["matches_played"] = csrr.get('losses') + csrr.get('wins')
            stats["wl"]             = csrr.get('wl')
            stats["kd"]             = csrr.get('kd')

            if stats.get("mmr_change") >= 0:
                stats["mmr_change"] = f'ᐃ{stats.get("mmr_change")}'
            else:
               stats["mmr_change"]  = f'ᐁ{abs(stats.get("mmr_change"))}'

        return stats

    def __generate_embed(self, stats):
        """
        --- Generating discord embed from user's stats
        """
        embed=discord.Embed(title="Tabstats",  url=stats.get("url"), color=0x039bba)

        embed.set_author(name=self.siege_name, url=stats.get("url"), icon_url=stats.get("avatar_url"))

        embed.set_thumbnail(url=stats.get("rank_url"))

        embed.add_field(name="Rank", value=stats.get("full_rank")[0:1].upper() + stats.get("full_rank")[1:], inline=False)
        
        if stats.get('matches_played'): # If user has not palyed this season, then footer with his MMR and KD will be None
            mmr = stats.get("mmr")
            mmr_change = stats.get('mmr_change')
            kd = stats.get('kd')
            wl = stats.get('wl')
            matches_played = stats.get('matches_played')

            stats = f"MMR: {mmr} {mmr_change} {9*' '} KD: {kd}\n{wl} wl in {matches_played} Matches"
            embed.set_footer(text=stats)

        return embed

    def parse_stats(self) -> discord.embeds.Embed:
        """
        --- Parsing users's stats from tabstats with requests
        """
        logging.info("Parsing data from r6.apitab.net")
        payload = {'display_name': self.__siege_name, 'platform': 'uplay'}
        r = requests.get('https://r6.apitab.net/website/search', params=payload)
        logging.info("Response received")
        if r.status_code != 200:
            logging.warning(f"Bad request. Status Code: {r.status_code}")
            return None
        try:
            stats = self.__unpack_stats(r)
            if self.__dID != 0:
                self.__siege_ID = stats.get("siege_ID")
                self.__rank = stats.get("rank")
            embed = self.__generate_embed(stats)
        except IndexError:
            if self.__dID != 0:
                User.delete_by_dID(self.__dID)
            embed=discord.Embed(title="User not found",  url="https://c.tenor.com/4IAtK3rSgBcAAAAd/that-is-so-tragic-gerald-broflovski.gif", color=0x039bba)
            logging.warning(f"This is message above: User not found. He's not authorized.")
        
        return embed


    def __repr__(self):
        return f'User(siege_name: "{self.__siege_name}", dID: "{self.__dID}", Siege ID: "{self.__siege_ID}", Siege ID: "{self.__rank}")'