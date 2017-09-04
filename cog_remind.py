from discord.ext import commands
import asyncio
from utils import *

class Remind():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def remind(self, ctx):
        getTime()
        args = ctx.message.content
        args = args.split(' ')
        try:
            if 's' in args[2]:
                time = int(args[2].replace('s', ''))
                await self.bot.say(f"Ok, I will remind you in {str(args[2].replace('s',''))} seconds to {str(args[1])}")
                await asyncio.sleep(time)
                await self.bot.send_message(ctx.message.author, f"You asked me to remind you to {str(args[1])} {str(time)} seconds from {str(getTime())}")
            elif 'm' in args[2]:
                time = int(args[2].replace('m', '')) * 60
                await self.bot.say(f"Ok, I will remind you in {str(args[2].replace('m',''))} minutes to {str(args[1])}")
                await asyncio.sleep(time)
                await self.bot.send_message(ctx.message.author, f"You asked me to remind you to {str(args[1])} {str(time)} seconds from {str(getTime())}")
            elif 'h' in args[2]:
                time = int(args[2].replace('h', '')) * 3600
                await self.bot.say(f"Ok, I will remind you in {str(args[2].replace('h',''))} hours to {str(args[1])}")
                await asyncio.sleep(time)
                await self.bot.send_message(ctx.message.author, f"You asked me to remind you to {str(args[1])} {str(time)} seconds from {str(getTime())}")
            else:
                await self.bot.say("You must put either s, m or h after your number!")
        except Exception as e:
            await self.bot.say("Your timer must include a number and either s,m or h.")

def setup(bot):
    bot.add_cog(Remind(bot))