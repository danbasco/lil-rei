import random
import re
import sqlite3

import asyncio

import discord
from discord import member
from discord.ext import commands
from imports import my_colour

import datetime as dt

from pymongo import MongoClient

con = sqlite3.connect("./cogs/money.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Upvoted(id INTEGER)''')

mc = MongoClient("mongodb+srv://danbas:lilrei2021app@myclusterrei.a2bkp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mc.get_database("databasel")
cluster = db.money

class Economia(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if not message.channel.id == 898714955770122240:
            return ...

        data = message.content.split(" ")
        user = int(re.sub("\D", "", data[2]))
        userdm = self.client.get_user(user)

        ##GET MONEY
        
        ran = random.randint(1000, 5000)
        try:
            cluster.find_one({"_id" : user})["money"]
            

        except:

            user_db = {
                "_id" : user,
                "money" : 0
            }
            
            cluster.insert_one(user_db)
        
        results = cluster.find_one({"_id" : user})["money"]
        
        
        update_money = {
            "money":ran+int(results)
        }
        cluster.update_one({"_id":user}, {"$set":update_money})

        money = cluster.find_one({"_id" : user})["money"]

        embed = discord.Embed(
            name="Upvote",
            colour=my_colour,
            description=f"Obrigado por dar suporte ao nosso bot! Com isso, você ganhou **{ran}** moedas! Lembre-se que pode votar mais vezes para ganhar mais!\n\nValor total de moedas: **{money}**",
            timestamp= dt.datetime.utcnow()
            )
        embed.set_author(name="Lil Rei Coins")

        await userdm.send(embed=embed)

        cur.execute(f'''INSERT INTO Upvoted(id) VALUES({user})''')
        asyncio.sleep(60*60*12)
        cur.execute(f'''DELETE FROM Upvoted WHERE id={user}''')


    @commands.command(name="money")
    async def money_command(self, ctx, user: discord.User = None):

        if user is None:
            user = ctx.author

        try:
            cluster.find_one({"_id" : user.id})["money"]
            
        except:

            user_db = {
                "_id" : user,
                "money" : 0
            }
            
            cluster.insert_one(user_db)

        money = cluster.find_one({"_id" : user.id})["money"]
        
        await ctx.send(f"O usuário **<@{user.id}>** possui **{money}** moedas!")


    @commands.command(name="upvote", aliases=["daily"])
    async def daily_command(self, ctx):

        cur.execute(f'''SELECT * FROM Upvoted WHERE id={ctx.author.id}''')
        user = cur.fetchone()

        if user == None:
            embed = discord.Embed(description="Gostaria de ganhar umas **moedas de graça e ainda ajudar o nosso bot?** Então clique [aqui](https://top.gg/bot/880584198358966303) para dar upvote na **Lil Rei e ainda ganhar moedas!**")

            return await ctx.send(embed=embed)

        await ctx.send("Você já deu upvote no bot! **Só pode votar de 12 em 12 horas!**")

    @commands.command(name="pay")
    async def pay_command(self, ctx, user: discord.User, value: int):

        if user == ctx.author:
            return await ctx.send("Você não pode mencionar a si mesmo!")
        
        try:
            cluster.find_one({"_id" : user.id})["money"]
            
        except:

            user_db = {
                "_id" : user.id,
                "money" : 0
            }
            
            cluster.insert_one(user_db)

        try:
            cluster.find_one({"_id" : ctx.author.id})["money"]
            
        except:

            user_db = {
                "_id" : ctx.author.id,
                "money" : 0
            }
            
            cluster.insert_one(user_db)

        user_pay = cluster.find_one({"_id" : ctx.author.id})["money"]
        user_recieve = cluster.find_one({"_id" : user.id})["money"]

        if value > user_pay:
            return await ctx.send("Você não possui dinheiro o suficiente para a transação!")
        
        
        msg = await ctx.send(f"**<@{ctx.author.id}> vai transferir {value} para <@{user.id}>**! Você deseja confirmar o pagamento?** ✅ ou :no_entry_sign:**")
        
        
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")    
        
        
        def check(reaction, member):
            return member == ctx.author and reaction.emoji in ["✅", "❌"]

        try:
            reaction, member = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
            
        except asyncio.TimeoutError:
            await ctx.send("Tempo limite esgotado!")
        
        else:
            
            if reaction.emoji == "✅":

                recieve = {
                    "money":user_recieve+value
                }

                pay = {
                    "money": user_pay-value
                }
                
                cluster.update_one({"_id": ctx.author.id}, {"$set": pay})
                cluster.update_one({"_id": user.id}, {"$set": recieve})

                await ctx.send(f"<@{ctx.author.id}> pagou {value} ao <@{user.id}>")

            elif reaction.emoji == "❌":
                
                await ctx.send("Foi cancelada a transação!")
        
    @pay_command.error
    async def pay_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Utilize `rei!pay <valor> <usuário>`")
    
    



def setup(client):
    client.add_cog(Economia(client))
