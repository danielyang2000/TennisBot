# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from RankScrape import scrape_rank

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

# @bot.event
# async def on_ready():
    
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break
#     print(f'{client.user} has connected to Discord!'
#             # f'{guild.name}(id: {guild.id})'    
#         )
#     print(guild.id)
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

def format_output(l):
    txt = "{:<8} {:<25} {:<8} {:<8} {:<8} {:<10} {:<10}" 
    return txt.format(*l)

@bot.command(name='top10rank', help='list top 10 ATP players')
async def nine_nine(ctx):
    print(ctx.author, 'used the rank command')
    response = format_output(['rank', 'name', 'point', 'age', 'country', 'height(cm)', 'weight (lbs)'])
    await ctx.send(response)
    rank = scrape_rank('https://www.atptour.com/en/rankings/singles')
    for i in range(10):
        response = format_output(next(rank))
        await ctx.send(response)

bot.run(TOKEN)