import discord
from discord.ext import commands
from utils import *
import sqlite3
import time



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


startup_extensions = ["cog_prefix", "cog_tags", "cog_remind", "cog_bank", "cog_games", "cog_profile", "cog_info"]
description = '''A multifunctional discord bot written in python, using the discord.py library.'''
bot = commands.Bot(command_prefix=get_pre, description=description)

bot.remove_command("help")
main_chan = discord.Object('354278428125429760')

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        time1 = time.strftime("%H hours %M minutes and %S seconds", time.gmtime(error.retry_after))
        await bot.send_message(ctx.message.channel, f"This command is on cooldown! Hold your horses! >:c\nTry again in {str(time1)}")
    else:
        await bot.send_message(main_chan, str(error) + " in channel " + ctx.message.channel.name + " in " + ctx.message.server.name + " issued by " + ctx.message.author.name + "#" + ctx.message.author.discriminator + ".")


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