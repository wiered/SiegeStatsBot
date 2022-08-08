import configparser

class Config:
    
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read('./SiegeDiscordBot/configs/config.ini')

        self.__token = self.__config.get('DEFAULT', 'token')
        self.__guild_id = int(self.__config.get('DEFAULT', 'guild_id'))
        self.__daily_update_log = int(self.__config.get('DEFAULT', 'daily_update_log'))
        self.__cl_defaul_channel = int(self.__config.get('DEFAULT', 'cl_defaul_channel'))
        self.__party_find_channel = int(self.__config.get('DEFAULT', 'party_find_channel'))

        self.__bot_avatar_url = self.__config.get('BOT', 'avatar_url')
        self.__bot_name = self.__config.get('BOT', 'bot_name')

    @property
    def token(self):
        return self.__token

    @property
    def guild_id(self):
        return self.__guild_id
    
    @property
    def daily_update_log(self):
        return self.__daily_update_log

    @property
    def cl_defaul_channel(self):
        return self.__cl_defaul_channel

    @property
    def party_find_channel(self):
        return self.__party_find_channel
    
    @property
    def bot_avatar_url(self):
        return self.__bot_avatar_url

    @property
    def bot_name(self):
        return self.__bot_name
