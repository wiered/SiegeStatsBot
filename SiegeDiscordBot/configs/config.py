"""
MIT License

Copyright (c) 2022 Artem Babka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
