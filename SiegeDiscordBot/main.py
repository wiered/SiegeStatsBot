import logging

# importing discord and setting up intents
import discord
from discord.ext import tasks
intents = discord.Intents(messages=True, guilds=True)


# importing parts
import parts.embeds as embeds
import parts.names_helpers as names_helpers
import parts.lobbys as lobbys
from parts.lobbys import Lobbys
from parts.daily_task import background_task

from authusers import User
from configs.config import Config

from bot_class import Bot

def main():
    # setting up logging and config
    logging.basicConfig(filename='./SiegeDiscordBot/logs/siegebot.log', filemode='w', format='[%(module)s: %(funcName)s: %(asctime)s: %(levelname)s] %(message)s', level=logging.INFO, encoding='utf-8')

    
    # Starting bot and loading data
    logging.info('Loading...')
    User.instantiate_from_csv() # Lodaing base from csv
    

    # Starting loops
    Bot.bot.loop.create_task(background_task())
    custom_lobby_loop.start()
    auto_save_loop.start()
    Bot.bot.run(config.token)
    

    # Saving data. Not working, i thing. See auto_save_loop()
    logging.info('Saving...')
    User.save_instance_to_csv() # Saving base to csv
    logging.info('Saved')

@tasks.loop(seconds=60)
async def custom_lobby_loop():
    """
    --- Task to remove custom lobbies
    """
    for lobby_id in Lobbys.all:
        lobby = Bot.bot.get_channel(lobby_id)
        if len(lobby.voice_states.keys()) != 0:
            continue

        logging.info(f'Deleting "{lobby.name}" voice channel. Reason: deleting empty lobby')
        await lobby.delete(reason = "Удаляю пустое лобби")
        Lobbys.remove_lobby(lobby_id)

@tasks.loop(seconds=1800)
async def auto_save_loop():
    """
    --- Autosaving task
    """
    logging.info('Autosaving...')
    User.save_instance_to_csv()
    logging.info('Autosaving completed')

@Bot.bot.command(pass_context=True)
async def auth(ctx, name: str = None):
    """
    --- Authorize in bot
    """
    if not name:
        logging.warning(f"{ctx.author.name} tried to authorize without name")
        await ctx.send("Не введено имя пользователя\n```w!auth [your siege name]```")
        return None

    logging.info(f"{ctx.author.name} trying to authorize with name {name}")

    if User.is_authorized(ctx.author.id):
        logging.info(f"But he is already authorized. So unfair")
        await ctx.send(embed = embeds.already_authorized_embed())
        return None

    user = User(name, ctx.author.id)
    embed, state = user.parse_stats()
    ref = discord.MessageReference(
        message_id=ctx.message.id,
        channel_id=ctx.channel.id, 
        guild_id=ctx.guild.id
        ) # Reference message
    if state:
        embed = embeds.succeseful_authorization()
    await ctx.send(embed=embed, reference=ref)
    logging.info(f"And he successfully authorized(maybe, cause i dont catch bad user name there, so look at message above). https://c.tenor.com/myWhE0y5rTsAAAAC/brent-rambo-thumbs-up.gif")

@Bot.bot.command(pass_context=True)
async def stats(ctx, value: str = None):
    """
    --- Get siege stats from tabstats
    """
    logging.info(f"{ctx.author.name} raising w!stats")
    user = User.get_by_dID(ctx.author.id)
    exeption_msg  = "You're not authorized."
    logger_msg = "He's not authorized"

    if value:
        logging.info(f"{ctx.author.name} raising w!stats with value: {value}!")
        exeption_msg  = "User not authorized."
        logger_msg = f"User {value} not authorized"
        user =  names_helpers.get_user_by(value)

    if not user:
        logging.warning(f"{ctx.author.name} raising w!stats but there is a problem: {logger_msg}!")
        await ctx.send(embed = embeds.unauthorized_embed(exeption_msg))
        return None

    embed, _ = user.parse_stats()
    ref = discord.MessageReference(
        message_id=ctx.message.id, 
        channel_id=ctx.channel.id, 
        guild_id=ctx.guild.id
        ) # Reference message
    await ctx.send(embed=embed, reference=ref)
    logging.info(f'Sent response to "w!stats {value}"')

@Bot.bot.command(pass_context=True)
async def party(ctx, value: int = None):
    """
    --- Create a party search announcement
    """

    logging.info(f"{ctx.author.name} want to created announcement in #поиск-пати")
    await ctx.message.delete()

    if ctx.message.channel.id != config.party_find_channel:
        logging.warning(f"But in wrong channel")
        await ctx.author.send(f"Поиск пати доступен только в канале #поиск-пати")
        return None

    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        logging.warning(f"But he's not in voice channel")
        await ctx.author.send("Вы не в голосовом канале")
        return None

    if not value:
        value = 5 - len(list(channel.voice_states.keys()))

    players, max_mmr = await lobbys.unpack_lobby(channel, ctx.guild)
    embed = embeds.generate_embed_for_party(
        f"Ищу +{value} в   {channel.name}",
        players, max_mmr-1000
        )
    await ctx.send(embed = embed)
    logging.info(f"Successfully created announcement in #поиск-пати")

@Bot.bot.command(pass_context=True)
async def lock(ctx):
    """
    --- Create private voice channel
    """
    logging.info(f"{ctx.author.name} want to create private room")
    category = ctx.guild.get_channel(config.cl_defaul_channel)
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        logging.warning(f"{ctx.author.name} is not in voice")
        await ctx.send("Вы не в голосовом канале")
        return None
        
    if not category:
        category = ctx.author.voice.channel.category
    else:
        category = category.category
        
    members      = list(channel.voice_states.keys())
    lim          = len(members)

    custom_lobby = await ctx.guild.create_voice_channel(ctx.author.name + "'s Lobby", overwrites=None, category=category, reason="Создаю лобби по запросу", user_limit = lim)
    logging.info(f"Succesefully created lobby")
    logging.info(f"Doing some discord bot things")
    overwrites = custom_lobby.overwrites_for(ctx.guild.default_role)
    overwrites.connect = False
    await custom_lobby.set_permissions(ctx.guild.default_role, overwrite=overwrites)
    
    overwrites = custom_lobby.overwrites_for(ctx.guild.default_role)
    overwrites.connect = True

    logging.info(f"Moving members to new voice channel")
    for member in members:
        _member = await ctx.guild.fetch_member(member)
        await ctx.channel.set_permissions(_member, overwrite=overwrites)
        await _member.move_to(custom_lobby, reason = "Перемещаю в лобби")
    Lobbys.add_lobby(custom_lobby.id)
    logging.info(f"Successfully created private channel to {ctx.author.name}")

@Bot.bot.command(pass_context=True)
async def help(ctx):
    logging.info(f"{ctx.author.name} want some help")
    await ctx.send(embed = embeds.help_embed())

@Bot.bot.event
async def on_ready():
    await Bot.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='w!help'))
    print("Ready!")
    logging.info("Bot is Ready!")

if __name__ == '__main__':
    config = Config()
    main()
    
