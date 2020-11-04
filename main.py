import requests
from bs4 import BeautifulSoup
import json
import discord
from discord.ext import commands
from discord.utils import get
import time
import asyncio


def getWinners():
    url = 'https://everipedia.org/oraqle/ap'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find('script')
    jsondict = json.loads(script.string)
    winners = jsondict['props']['pageProps']['allWinners']

    finalwinners = {}
    for state in winners:
        finalwinners[state] = winners[state]['president']
    
    return finalwinners


TOKEN = 'lol token bruh'
BOTID = 'id lol'
bot = commands.Bot(command_prefix="election.")


def createMessage():

    electoral = {
        'CA':55,
        'OR':7,
        'WA':12,
        'NV':6,
        'UT':6,
        'AZ':11,
        'ID':4,
        'MT':3,
        'WY':3,
        'CO':9,
        'NM':5,
        'ND':3,
        'SD':3,
        'NE':5,
        'KS':6,
        'OK':7,
        'TX':38,
        'MN':10,
        'IA':6,
        'MO':10,
        'AR':6,
        'LA':8,
        'WI':10,
        'IL':20,
        'MS':6,
        'IN':11,
        'OH':18,
        'KY':8,
        'AL':9,
        'GA':16,
        'FL':29,
        'SC':9,
        'NC':15,
        'VA':13,
        'WV':5,
        'PA':20,
        'NY':29,
        'VT':3,
        'NH':4,
        'ME':4,
        'MA':11,
        'RI':4,
        'CT':7,
        'NJ':14,
        'DE':3,
        'MD':10,
        'DC':3,
        'AK':3,
        'HI':4,
        'TN':11
    }

    winners = getWinners()
    message = ''
    trump = 0
    biden = 0
    for state in winners:
        if state == 'US':
            message += f'**{state}: {winners[state]}**'
        else:
            message += f'\n{state}: {winners[state]}'
            if winners[state] == 'Trump':
                trump += electoral[state]
            elif winners[state] == 'Biden':
                biden += electoral[state]
    message += f'\n\nTrump: {trump} \nBiden: {biden}'
    return message

async def editMessage():
    f = open('balls.txt')
    channels = eval(f.read())
    print('edited!')
    for channelid in channels:
        channel = get(bot.get_all_channels(), id=int(channelid))
        messages = await channel.history().flatten()
        messageobj = get(messages, author=bot.user)
        content = createMessage()
        await messageobj.edit(content=content)



@bot.command()
@commands.has_permissions(administrator=True)
async def results(ctx):
    f = open('balls.txt', 'r+')
    channels = eval(f.read())
    f.seek(0)
    if ctx.channel.id in channels:
        channels.remove(ctx.channel.id)
    else:
        channels.append(ctx.channel.id)
        message = createMessage()

        await ctx.send(message)
    f.write(str(channels))
    f.truncate()
    f.close()

@bot.command()
@commands.has_permissions(administrator=True)
async def start(ctx):
    while True:
        await editMessage()
        await asyncio.sleep(300)


bot.run(TOKEN)
