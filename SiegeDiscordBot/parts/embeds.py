"""
--- This library contains helpers
"""

import discord

def generate_embed_for_party(title, players, min_mmr):
    """
    --- Generates embed for party
    """
    embed=discord.Embed(title=title, color=0x039bba)
    embed.set_thumbnail(url='https://lobby.rainbow6.ru/vd5ff194/lobby/0/0/0/preview.png')
    embed.add_field(name="Players:", value=players, inline=False)
    embed.set_footer(text=f'от {min_mmr} mmr')
    return embed

def help_embed():
    avatar_url = "https://cdn.discordapp.com/app-icons/840814724715380787/f6641ac04de80fdae4962afbd1153b51.png?size=512"
    embed=discord.Embed(description = "Some help if you want", color=0x039bba)
    
    embed.set_author(name="WaifuBot | R6Hub • Help", url="https://github.com/wiered/SiegeStatsBot", icon_url=avatar_url)
    embed.set_thumbnail(url=avatar_url)

    embed.add_field(name="R6Stats", value="`w!auth`, `w!stats`", inline=False)
    embed.add_field(name="Party commands", value="`w!party`, `w!lock`", inline=False)

    embed.set_footer(text="WaifuBot • R6Hub", icon_url=avatar_url)
    return embed