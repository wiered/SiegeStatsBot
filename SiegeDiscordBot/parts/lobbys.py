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