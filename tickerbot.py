import discord
import yahoo_fin.stock_info as si
import asyncio
import pandas as pd

from discord.ext import commands

client = discord.Client()


@client.event
async def on_ready():
    print("bot is ready")

async def checkStock():
    await client.wait_until_ready()

    ticker = "TICKER"

    while True:

        print(si.get_live_price(ticker))

        temp = si.get_quote_table(ticker)
        change = round(temp["Quote Price"] - temp["Previous Close"], 2)
        percentage = round(change / temp["Previous Close"] * 100, 2)

        displayQuote = str(round(temp["Quote Price"], 2))
        displayChange = str(change)
        displayPercentage = str(percentage)
        symbol = "\u2198"
        rocket = ""

        server = client.get_guild('server ID')

        if change >= 0:
            displayChange = "+" + displayChange
            displayPercentage = "+" + displayPercentage
            symbol = "\u2197"

            for role in server.roles:
                if role.name == ticker:
                    await role.edit(colour=0x00ff00)

            if percentage >= 5:
                rocket = "\U0001F680"


        else:

            for role in server.roles:
                if role.name == ticker:
                    await role.edit(colour=0xff0000)

        await server.me.edit(nick=displayQuote)
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{displayChange} ({displayPercentage}%) {symbol} {rocket}"))

        await asyncio.sleep(10)



client.loop.create_task(checkStock())


client.run('TOKEN')
