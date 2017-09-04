import discord
from discord.ext import commands
from utils import *
import sqlite3
import time
import aiohttp
import discord
import asyncio

async def my_background_task():
    await bot.wait_until_ready()
    counter = 0
    channel = discord.Object(id='354278428125429760')
    while not bot.is_closed:
        guild_count = len(bot.servers)
        # replace guilds with servers if you're on async and not rewrite
        headers = {
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI0MzkyMzUxNzQ4NDE3MTI3NCIsImlhdCI6MTUwNDU0MDY5MX0.SJUcrnBjrcirz9POGLRqUooIuSw9bdeTNKh4osL6lCk'}
        data = {'server_count': guild_count}
        api_url = 'https://discordbots.org/api/bots/354007795424690196/stats'
        async with aiohttp.ClientSession() as session:
            await session.post(api_url, data=data, headers=headers)
        await bot.send_message(channel, counter)
        await asyncio.sleep(600)

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


startup_extensions = ["cog_prefix", "cog_tags", "cog_remind", "cog_bank", "cog_games", "cog_profile", "cog_info", "cog_custom"]
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
async def on_server_join(server):
    try:
        invites = await bot.invites_from(server)
        for invite in invites:
            if not invite.revoked:
                code = invite.code
                break
    except Exception:
        code = "I couldn't grab an invite."
    await bot.send_message(main_chan, '[`'+str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"))+'`] I joined the server `' + server.name + '` ('+ server.id + '), owned by `' + server.owner.name + '#' + server.owner.discriminator + '` (' + server.owner.id + '). First invite I could find: {}'.format(code))

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

@bot.event
async def on_message(message):
    connectcustom()

    conn = sqlite3.connect("custom.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM custom WHERE guildid=?", (message.server.id,))
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        if message.content == row[4]:
            msgToSend = str(row[3])
            if '{tagAuthor}' in msgToSend:
                toSend = msgToSend.replace('{tagAuthor}', message.author.mention)
                if '{channel}' in msgToSend:
                    toSend1 = toSend.replace('{channel}', message.channel.name)
                    send = False
                else:
                    send = True

            if send:
                await bot.send_message(message.channel, toSend)
            else:
                await bot.send_message(message.channel, toSend1)

    await bot.process_commands(message)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

token = open("token.txt", "r")
toke = token.read()
bot.loop.create_task(my_background_task())
bot.run(str(toke))