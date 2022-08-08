from authusers import User
import re
import discord

def get_name(member):
    name = member.nick
    if not name:
        name = member.name
    return name

def get_user_by(name):
    """
    --- Get authorized user by discord tag
        or
        Create user by name
    """
    match = re.search(r'<@(\d{18})>', name)
    if match:
        return User.get_by_dID(int(match.group(1)))
    else:
        return User(name)

def check_nick(nick, name):
    """
    --- Checks if user's nickname contains 🔗
    """
    if not nick:
        return name + "🔗"
    else:
        if "🔗" in nick:
            return nick
        else:
            return nick + "🔗"

async def change_name(member):
    """
    --- Change 'R6Hub' guild members's name
    """
    nick = check_nick(member.nick, member.name)
    try:
        await member.edit(reason=None, nick = nick)
    except discord.errors.Forbidden:
        print("discord.errors.Forbidden: Missing Permissions i think")