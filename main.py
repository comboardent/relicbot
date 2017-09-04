import discord
from discord.ext import commands
from utils import *
import sqlite3

async def get_pre(bot, message):
    connect()
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM prefix WHERE guildid=?", (message.server.id,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return "!"
    else:
        return [(rows[0][1]), "!"]


startup_extensions = ["cog_prefix", "cog_tags", "cog_remind", "cog_bank", "cog_games"]
description = '''A multifunctional discord bot written in python, using the discord.py library.'''
bot = commands.Bot(command_prefix=get_pre, description=description)

@bot.event
async def on_ready():
    server_count = 0
    for s in bot.servers:
        server_count = server_count + 1
    print('Logged in as')
    print(bot.user.name)
    print("Server count " + str(server_count))
    await bot.change_presence(game=discord.Game(name="!help"))
    print('------')

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

token = open("token.txt", "r")
toke = token.read()

bot.run(str(toke))