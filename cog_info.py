import discord
from discord.ext import commands
from utils import *

class Info():
    def __init__(self, bot):
        self.bot=bot
    @commands.command(pass_context=True)
    async def help(self, ctx):


        commands = len(self.bot.commands)
        embed = discord.Embed(title="The bot prefix for this server is: " + str(getPrefix(ctx.message.server.id)),
                              color=ctx.message.author.color)
        embed.add_field(name="Bank",
                        value="`Balance`, `Broke`, `CreateAccount`,",
                        inline=False)
        embed.add_field(name="Games",
                        value="`Bet`, `CoinFlip`, `Slots`",
                        inline=False)
        embed.add_field(name="Prefix", value="`prefix`, `prefix view`, `prefixset`",
                        inline=False)
        embed.add_field(name="Profile", value="`profile view`, `profile create`, `reputation`, `reputation add`",
                        inline=False)
        embed.add_field(name="Tag", value="`tag create`, `tag delete`, `tag edit`, `tag view`",
                        inline=False)
        embed.set_footer(
            text="Requested by " + ctx.message.author.display_name + " | Total commands: " + str(commands))
        await self.bot.send_message(ctx.message.channel, content=None, embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))