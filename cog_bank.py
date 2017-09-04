import discord
from discord.ext import commands
from utils import *

class Bank():
    def __init__(self, bot):
        self.bot=bot

    @commands.command(pass_context=True, aliases=["ca"])
    async def createaccount(self, ctx):
        connectbank()
        userid = ctx.message.author.id
        conn = sqlite3.connect("money.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM bank")
        rows = cur.fetchall()
        conn.close()
        if any(userid in s for s in rows):
            await self.bot.say("You already have an account!")
        else:
            connectbank()
            conn = sqlite3.connect("money.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO bank VALUES(?, ?)", (userid, 25))
            conn.commit()
            conn.close()
            await self.bot.say("Successfully opened an account for you with a balance of 25!")

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        connectbank()
        if len(ctx.message.mentions) == 0:
            try:
                if int((balance(ctx.message.author.id))) == 0:
                    await self.bot.say("You are broke :( Use !broke to get 5 free coins!")
                else:
                    await self.bot.say(str(balance(ctx.message.author.id)) + " coins")
            except:
                await self.bot.say("This user doesn't have an account")
        else:
            userid = ctx.message.mentions[0].id
            connectbank()
            conn = sqlite3.connect("money.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM bank WHERE user=?", (userid,))
            rows = cur.fetchall()
            conn.commit()
            conn.close()
            if not rows:
                await self.bot.say("That user doesn't have an account, he can make one with !createaccount.")
            else:
                await self.bot.say(ctx.message.mentions[0].name + "'s balance is " + str(rows[0][1]))

    @commands.command(pass_context=True)
    async def broke(self, ctx):
        if int(balance(ctx.message.author.id)) == 0:
            addmoney(ctx.message.author.id, 5)
            await self.bot.say("5 coins have been added to your account.")
        else:
            await self.bot.say("You have to be broke (0 coins) to use this command!")


def setup(bot):
    bot.add_cog(Bank(bot))