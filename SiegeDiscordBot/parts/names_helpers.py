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
