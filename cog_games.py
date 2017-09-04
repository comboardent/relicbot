from discord.ext import commands

from utils import *
import random

class Extras():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bet(self, ctx, amount=None):
        if hasAccount(ctx.message.author.id):
            bal = balance(ctx.message.author.id)
            try:
                if int(amount) > int(bal):
                    await self.bot.say("You can't bet more than you have!")
                else:
                    await self.bot.say("Do you pick 1 or 2?")
                    cont = await self.bot.wait_for_message(author=ctx.message.author)
                    if cont.content == "1" or cont.content == "2":
                        winner = random.randint(1, 2)
                        if winner == int(cont.content):
                            addmoney(ctx.message.author.id, int(amount))
                            await self.bot.say("You won " + str(amount) + " coins!")
                        else:
                            removemoney(ctx.message.author.id, int(amount))
                            await self.bot.say("You lost " + str(amount) + " coins :(")
                    else:
                        await self.bot.say("You must enter either 1 or 2!")
            except:
                await self.bot.say("You need to bet an amount(number)!")
        else:
            await self.bot.say("You need a bank account, create one with !createaccount!")

    @commands.command(pass_context=True)
    async def coinflip(self, ctx, amount=None):
        if hasAccount(ctx.message.author.id):
            bal = balance(ctx.message.author.id)
            try:
                if int(amount) > int(bal):
                    await self.bot.say("You can't bet more than you have!")
                else:
                    await self.bot.say("Do you pick heads or tails?")
                    cont = await self.bot.wait_for_message(author=ctx.message.author)
                    if cont.content.lower() == "heads" or cont.content.lower() == "tails":
                        if flip() == cont.content.lower():
                            await self.bot.say("You won the bet! " + str(amount) + " coins added to your balance!")
                            addmoney(ctx.message.author.id, int(amount))
                        else:
                            await self.bot.say("You lost " + str(amount) + " coins :(")
                            removemoney(ctx.message.author.id, int(amount))
            except:
                await self.bot.say("You need to bet an amount(number)!")
        else:
            await self.bot.say("You need a bank account, create one with !createaccount!")

    @commands.command(pass_context=True)
    async def slots(self, ctx, amount=None):
        if amount is None:
            await self.bot.say("You need to bet an amount(number)")
        else:
            if hasAccount(ctx.message.author.id):
                bal = balance(ctx.message.author.id)
                amounttrip = (int(amount) * 3)
                amountdoub = (int(amount) * 2)
                try:
                    if int(amount) > int(bal):
                        await self.bot.say("You can't bet more than you have!")
                    else:
                        var1 = int(random.random() * 5)
                        var2 = int(random.random() * 5)
                        var3 = int(random.random() * 5)
                        var4 = int(random.random() * 5)
                        var5 = int(random.random() * 5)
                        var6 = int(random.random() * 5)
                        var7 = int(random.random() * 5)
                        var8 = int(random.random() * 5)
                        var9 = int(random.random() * 5)
                        col = [":moneybag:", ":cherries:", ":carrot:", ":popcorn:", ":seven:"]
                        if var6 == var5 and var5 == var4 and var4 == var6:
                            msg = "**You won triple your money!!**"
                            addmoney(ctx.message.author.id, amounttrip)
                        elif var6 == var5 and var5 == var4:
                            msg = "**You won double your money!!**"
                            addmoney(ctx.message.author.id, amountdoub)
                        elif var6 == var5:
                            msg = "**You won double your money!!**"
                            addmoney(ctx.message.author.id, amountdoub)
                        elif var5 == var4:
                            msg = "**You won double your money!!**"
                            addmoney(ctx.message.author.id, amountdoub)
                        elif var6 == var4:
                            msg = "**You won double your money!!**"
                            addmoney(ctx.message.author.id, amountdoub)
                        else:
                            msg = ("**You lost!** " + str(amount) + " coins down the drain")
                            removemoney(ctx.message.author.id, amount)
                        await self.bot.say(
                            "{0}\n\n{1}{2}{3}\n{4}{5}{6} :arrow_left:\n{7}{8}{9}".format(msg, col[var1], col[var2],
                                                                                         col[var3],
                                                                                         col[var4], col[var5], col[var6],
                                                                                         col[var7],
                                                                                         col[var8], col[var9]))
                except Exception as e:
                    print(str(e))
            else:
                await self.bot.say("You need a bank account, create one with !createaccount!")


def setup(bot):
    bot.add_cog(Extras(bot))
