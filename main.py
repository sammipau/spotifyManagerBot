import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from spotifyManager import SpotifyManager

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.command()
async def addRecent(ctx):
    # hard code my spotify for now, then try to add auth via discord
    # hard code which playlist for now
    manager = SpotifyManager()
    if not manager.fail:
        count = manager.add_recent()
        if count == 'Error':
            await ctx.send(f'Error adding recent')
        if count != 0:
            await ctx.send(f'Successfully added {count} songs.')
        else:
            await ctx.send(f'No new songs detected.')
    else:
        await ctx.send(f'Error adding recent')

@bot.command()
async def removeOld(ctx):
    # hard code my spotify for now, then try to add auth via discord
    # hard code which playlist for now
    manager = SpotifyManager()
    if not manager.fail: 
        count = manager.remove_old()
        if count != 0:
            await ctx.send(f'Successfully removed {count} songs.')
        else:
            await ctx.send(f'No old songs detected.')
    else:
        await ctx.send(f'Error removing old songs.')

@bot.command()
async def list(ctx):
    command_list = bot.commands
    response = "You can use the following commands:\n"
    for command in command_list:
        response += f"~{command.name} - {command.help}\n"

    await ctx.send(response)

load_dotenv()
bot.run(os.getenv('TOKEN'))