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

from authusers import User

class Lobbys:
    all = []
    
    @staticmethod
    def add_lobby(lobby):
        Lobbys.all.append(lobby)

    @staticmethod
    def remove_lobby(lobby):
        if lobby in Lobbys.all:
            Lobbys.all.remove(lobby)

def get_user_data(user, member, players, max_mmr):
    """
    --- Generate userdata and mention
    """
    if not user:
        return f"{players} {member.mention}\n", max_mmr
    else:
        stats = user.parse_stats().to_dict() # user.parse_stats() returns discord.Embed, so i unpacking to dict
        rank = stats.get('fields')[0].get('value').capitalize()
        mmr = int(stats.get('footer').get('text')[5:9])
        if mmr > max_mmr:
            max_mmr = mmr
        return f'{players} {member.mention} - `{rank}` `{mmr} MMR`\n', max_mmr


async def unpack_lobby(channel, guild):
    """
    --- Get all members in voice channel 
        and set lobbys's max mmr
    """
    members = list(channel.voice_states.keys())
    players = ""
    max_mmr = 0
    for member in members:
        member = await guild.fetch_member(member)
        user = User.get_by_dID(member.id)
        players, max_mmr = get_user_data(user, member, players, max_mmr)
    return players, max_mmr
