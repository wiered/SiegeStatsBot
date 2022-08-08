from discord.ext import commands

class Bot:
    bot = commands.Bot(command_prefix = "w!")
    bot.remove_command('help')