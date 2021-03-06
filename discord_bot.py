import discord
import os
from main import *
from keep_alive import keep_alive

bot_key = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$steamersect'):
        # get list from comma delimited steam ids
        id_string = message.content.split("$steamersect ", 1)[1]
        id_string = id_string.replace(" ", "")
        ids = id_string.split(',')

        names = interface_player_names(ids)
        intersect = interface_intersect(ids)
        majority = interface_majority(ids)

        await message.channel.send("players: {}".format(convert_ids_to_string(names)))

        await message.channel.send("intersection")
        for game in intersect:
          await message.channel.send(game)
          
        await message.channel.send("majority")
        for game in majority:
          await message.channel.send(game)

keep_alive()
client.run(bot_key)