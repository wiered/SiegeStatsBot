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

import asyncio
import logging
from datetime import datetime, time, timedelta

import parts.names_helpers as names_helpers
import parts.dicts as dicts
from configs.config import Config

from authusers import User
from bot_class import Bot

config = Config()

daily_update_time = time(3, 0, 0)

async def change_role(user, old_rank, rank):
    """
    --- Change 'R6Hub' guild members's rank role
    """
    guild        = await Bot.bot.fetch_guild(config.guild_id)
    member       = await guild.fetch_member(user.dID)
    if not member:
        return None
    role0 = guild.get_role(dicts.roles_Ids[old_rank])
    role1 = guild.get_role(dicts.roles_Ids[rank])
    await member.remove_roles(role0)
    await member.add_roles(role1)

async def daily_update():
    """
    --- Daily task to update users rank roles on 'R6Hub' guild
    """
    logging.info('Starting daily update...')
    channel = Bot.bot.get_channel(config.daily_update_log)
    for user in User.all:
        old_rank = user.rank
        embed = user.parse_stats()

        guild    = await Bot.bot.fetch_guild(config.guild_id)
        member   = await guild.fetch_member(user.dID)
        if member:
            await names_helpers.change_name(member)
            if old_rank != user.rank:
                await change_role(user, old_rank, user.rank)
        await channel.send(embed=embed) # Sending embed
    User.save_instance_to_csv()
    logging.info('Data updatet succesefully')

async def background_task():
    """
    --- Just sleeping untill 6am Moscow (3am utc)
        then calling daily_update()
    """
    logging.info('Starting up daily task...')
    now = datetime.utcnow()
    logging.info(f'Getted now time: {now}')
    if now.time() > daily_update_time:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds  = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        logging.info(f'daily task sleeping')
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        logging.info(f'daily task main loop')
        now                  = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time          = datetime.combine(now.date(), daily_update_time)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await daily_update()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds  = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration
