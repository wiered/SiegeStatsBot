"""
--- Embed generators
"""

import discord
from configs.config import Config


config = Config()
bot_avatar_url = config.bot_avatar_url
bot_name = config.bot_name

def generate_embed_for_party(title, players, min_mmr):
    """
    --- Generate embed for search party announcment
    """
    embed = discord.Embed(title=title, color=0x039bba)
    embed.set_thumbnail(url='https://lobby.rainbow6.ru/vd5ff194/lobby/0/0/0/preview.png')
    embed.add_field(name="Players:", value=players, inline=False)
    embed.set_footer(text=f'от {min_mmr} mmr')
    return embed

def help_embed():
    """
    --- Generate embed with help
    """
    
    embed = discord.Embed(description = "Some help if you want", color=0x039bba)
    
    embed.set_author(name=f"{bot_name} | R6Hub • Help", url="https://github.com/wiered/SiegeStatsBot", icon_url=bot_avatar_url)
    embed.set_thumbnail(url=bot_avatar_url)

    embed.add_field(name="R6Stats", value="`w!auth`, `w!stats`", inline=False)
    embed.add_field(name="Party commands", value="`w!party`, `w!lock`", inline=False)

    embed.set_footer(text=f"{bot_name} • R6Hub", icon_url=bot_avatar_url)
    return embed

def unauthorized_embed(exception_msg):
    """
    --- Generate embed with unauthorized member exeption
    """

    embed = discord.Embed(title = f"{exception_msg}", color=0x039bba)

    embed.add_field(name="`w!auth <r6 name>`", value="For authorize", inline=False)
    embed.add_field(name="`w!help`", value="For more", inline=False)

    embed.set_footer(text=f"{bot_name} • R6Hub", icon_url=bot_avatar_url)
    return embed

def succeseful_authorization():
    """
    --- Generate succeseful authorization embed
    """

    embed = discord.Embed(title = "Succesefully authorised!", color=0x039bba)
    embed.set_footer(text=f"{bot_name} • R6Hub", icon_url=bot_avatar_url)

def already_authorized_embed(exception_msg):
    """
    --- Generate embed with unauthorized member exeption
    """

    embed = discord.Embed(title = "You already authorized", color=0x039bba)

    embed.add_field(name="`w!help`", value="For more", inline=False)

    embed.set_footer(text=f"{bot_name} • R6Hub", icon_url=bot_avatar_url)
    return embed