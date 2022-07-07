import discord
import os
from main import *

bot_key = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')
    if message.content.startswith('$steamersect'):
        # get list from comma delimited steam ids
        id_string = message.content.split("$steamersect ", 1)[1]
        ids = id_string.split(',')

        print(ids)

        intersect = interface_intersect(ids)
        majority = interface_majority(ids)
      
        await message.channel.send("intersection")
        for game in intersect:
          await message.channel.send(game)
          
        await message.channel.send("majority")
        for game in majority:
          await message.channel.send(game)

client.run(bot_key)