# bot.py
import os
import time
import datetime as dt

import discord
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from RankScrape import scrape_rank

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!tb_')

scrape_url = 'https://www.atptour.com/en/rankings/singles?rankRange=1-5000'
scrape_url_top100 = 'https://www.atptour.com/en/rankings/singles'
image_prefix = 'https://www.atptour.com'
empty_image = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# def format_output(l):
#     txt = "{:<8} {:<25} {:<8} {:<8} {:<8} {:<10} {:<10}" 
#     return txt.format(*l)

# print command usage info to log 
def command_user(ctx):
    print('{} used the \'{}\' in \'{}\' channel of \'{}\''.format(ctx.author, ctx.command, ctx.channel, ctx.guild))
    print('^^^time =', time.strftime('%X'))
    print('message =', ctx.message.content)

# @bot.command(name='top10rank', help='list top 10 ATP players')
# async def nine_nine(ctx):
#     command_user(ctx)
#     response = format_output(['rank', 'name', 'point', 'age', 'country', 'height(cm)', 'weight (lbs)'])
#     await ctx.send(response)
#     rank = scrape_rank('https://www.atptour.com/en/rankings/singles', command='top10')
#     while True:
#         try:
#             response = format_output(next(rank))
#             await ctx.send(response)
#         except StopIteration:
#             break


# build embed based on initial embed heading and iterable of player info
async def build_embed(embed, rank):
    first = True
    # file= None
    for rk, name, pts, age, flag, ht, wt, pl, img in rank:
        if first:
            if img is None:
                embed.set_image(url=empty_image)
            else:
                embed.set_image(url=image_prefix+img)
            first = False
        embed.add_field(name=f'**No.{rk}: {name} ({pts})**', value=f'\n\n\n> [link]({pl})\n> age: {age}\n> flag: {flag}\n> height(cm): {ht}\n> weight(lbs): {wt}\n\n',inline=False)
    return embed

# Scrape top 10 ATP players
@bot.command(name='top10', help='list top 10 ATP players')
async def nine_nine(ctx):
    command_user(ctx)
    await ctx.send("extracting...")

    embed = discord.Embed(title=f"__**Current top 10 players:**__", color=0x03f8fc,timestamp= ctx.message.created_at)
    rank = scrape_rank(scrape_url, command='top10')
    
    embed = await build_embed(embed, rank)
    await ctx.send(embed=embed)

# scrape players based on ranks specified by users
@bot.command(name='rank', help='\'rank\' x,y,z,... prints player one by one from high rank to low rank')
async def rank_spec(ctx, rank):
    command_user(ctx)
    await ctx.send('formating...')

    embed = discord.Embed(title=f"__**Chosen rank:**__", color=0xff0000,timestamp= ctx.message.created_at)
    try:
        rank = scrape_rank(scrape_url, command='spec ' + str(rank))
        embed = await build_embed(embed, rank)
        await ctx.send(embed=embed)
    except:
        await ctx.send(f"rank number has to be integer: {ctx.message.content}")
    
target_channel_ids = [977292185319911467, 688950889738010669, 524687944917712896]

# weekly ranking updates
@tasks.loop(hours=168)
async def called_once_a_week():
    rank = scrape_rank(scrape_url, command='top10')

    embed = discord.Embed(title=f"__**!New top 10 Ranking!**__", color=0x03f8fc)#,timestamp= ctx.message.created_at)

    embed = await build_embed(embed, rank)
    for id in target_channel_ids:
        message_channel = bot.get_channel(id)
        await message_channel.send("!!! WEEKLY RANKING UPDATE !!!")
        await message_channel.send(embed=embed)

    print("Finished weekly ranking update")

@called_once_a_week.before_loop
async def before():
    # loop the whole 7 day (60 sec 60 min 24 hours 7 days)
    for _ in range(60*60*24*7):  
        if dt.datetime.utcnow().strftime("%H:%M UTC %a") == "13:30 UTC Mon":
            print('time for weekly update')
            return

        # wait some time before another loop. Don't make it more than 60 sec or it will skip
        await asyncio.sleep(30)
    # await asyncio.sleep(295200)
    # print("Finished waiting")
    # await bot.wait_until_ready()

called_once_a_week.start()

bot.run(TOKEN)