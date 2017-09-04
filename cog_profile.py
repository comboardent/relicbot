from utils import *
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

#@commands.cooldown(rate,per,BucketType.user)
class Profile():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Profile sub-commands", color=ctx.message.author.color)
            embed.add_field(name=getPrefix(ctx.message.server.id)+"profile create", value="Create a new profile!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "profile view", value="View someone elses profile!", inline=False)
            await self.bot.say(embed=embed)

    @profile.command(pass_context=True)
    async def create(self, ctx):
        try:
            connectprofile()
            conn = sqlite3.connect("profile.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile WHERE userid=?", (ctx.message.author.id,))
            rows = cur.fetchall()
            conn.close()
            if not rows:
                if hasAccount(ctx.message.author.id):
                    bal = str(balance(ctx.message.author.id))
                else:
                    bal = "The user doesn't have a bank account"
                conn = sqlite3.connect("profile.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO profile VALUES(?, ?, ?)", (ctx.message.author.id, 0, str(bal)))
                conn.commit()
                conn.close()
                await self.bot.say("Successfully created a profile for you!")
            else:
                await self.bot.say("You already have a profile!")
        except Exception as e:
            print(str(e))

    @profile.command(pass_context=True)
    async def view(self, ctx):

        if len(ctx.message.mentions) == 0:
            if hasProfile(ctx.message.author.id):
                connectprofile()
                conn = sqlite3.connect("profile.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM profile WHERE userid=?", (ctx.message.author.id,))
                rows = cur.fetchall()
                conn.close()
                embed = discord.Embed(title=f"{ctx.message.author.name}'s profile", color=ctx.message.author.color)
                embed.add_field(name="Reputation", value=str(rows[0][1]))
                embed.add_field(name="Balance", value=str(rows[0][2]))
                await self.bot.say(embed=embed)
            else:
                await self.bot.say(f"You don't have a profile, create one with {getPrefix(ctx.message.server.id)}profile create")
        else:
            if hasProfile(ctx.message.mentions[0].id):
                connectprofile()
                conn = sqlite3.connect("profile.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM profile WHERE userid=?", (ctx.message.mentions[0].id,))
                rows = cur.fetchall()
                conn.close()
                embed = discord.Embed(title=f"{ctx.message.mentions[0].name}'s profile", color=ctx.message.author.color)
                embed.add_field(name="Reputation", value=str(rows[0][1]))
                embed.add_field(name="Balance", value=str(rows[0][2]))
                await self.bot.say(embed=embed)
            else:
                await self.bot.say(f"{ctx.message.mentions[0].name} doesn't have a profile.")


    @commands.group(pass_context=True)
    #    @commands.cooldown(1,43200,BucketType.user)
    async def reputation(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Reputation sub-commands", color=ctx.message.author.color)
            embed.add_field(name=getPrefix(ctx.message.server.id)+"reputation view", value="View your reputation!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "reputation add", value="Increase someones else reputation!", inline=False)
            await self.bot.say(embed=embed)

    @reputation.command(pass_context=True)
    async def points(self, ctx):
        try:
            if len(ctx.message.mentions) == 0:
                if hasProfile(ctx.message.author.id):
                    connectprofile()
                    conn = sqlite3.connect("profile.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM profile WHERE userid=?", (ctx.message.author.id,))
                    rows = cur.fetchall()
                    conn.close()
                    await self.bot.say(f"{ctx.message.author.name}'s reputation is {str(rows[0][1])}")
                else:
                    await self.bot.say("You don't have any reputation!")
            else:
                if hasProfile(ctx.message.mentions[0].id):
                    connectprofile()
                    conn = sqlite3.connect("profile.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM profile WHERE userid=?", (ctx.message.mentions[0].id,))
                    rows = cur.fetchall()
                    conn.close()
                    await self.bot.say(f"{ctx.message.mentions[0].name}'s reputation is {str(rows[0][1])}")
                else:
                    await self.bot.say(f"{ctx.message.mentions[0].name} doesn't have any reputation!")
        except Exception as e:
            print(str(e))

    @reputation.command(pass_context=True)
    @commands.cooldown(1,43200,BucketType.user)
    async def add(self, ctx):
        try:
            if len(ctx.message.mentions) == 0:
                await self.bot.say("You must choose someone to add your reputation to!")
            else:
                userToAdd = ctx.message.mentions[0].id
                if hasProfile(userToAdd):
                    connectprofile()
                    conn = sqlite3.connect("profile.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM profile WHERE userid=?", (ctx.message.mentions[0].id,))
                    rows = cur.fetchall()
                    conn.close()
                    rep = int(rows[0][1])
                    newRep = rep + 1
                    bal = balance(userToAdd)
                    conn = sqlite3.connect("profile.db")
                    cur = conn.cursor()
                    cur.execute("UPDATE profile SET reputation=?, balance=? WHERE userid=?", (int(newRep), int(bal), ctx.message.mentions[0].id))
                    conn.commit()
                    conn.close()
                    await self.bot.say(f"Successfully added 1 reputation to {ctx.message.mentions[0].name}")
                else:
                    await self.bot.say("That user doesn't have a profile so you can't add reputation to them!")
        except Exception as e:
            print(str(e))




def setup(bot):
    bot.add_cog(Profile(bot))