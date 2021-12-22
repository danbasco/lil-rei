from sqlite3.dbapi2 import Timestamp
from imports import *


import sqlite3

con = sqlite3.connect("./cogs/photos.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Photos(rei TEXT, kiss TEXT )''')

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="fala", aliases= ["say, speak"])
    async def fala_command(self, ctx, *, args):
        
        mensagem = str(args)

        if "@" in mensagem:
            
            await ctx.send("Tentando burlar o sistema? Não use menções dentro do bot!")
            
        else:    
            
            await ctx.send(mensagem)
            await ctx.message.delete()

    @commands.command(name="randomrei")
    async def randomrei_command(self, ctx):
        msg = random.choice(rei_photo)

        embed = discord.Embed(
            title= "Ayanami Rei",
            description=f"[Clique aqui para baixar a imagem!]({msg})",
            colour= my_colour,
            timestamp= dt.datetime.utcnow()
            )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        embed.set_image(url= msg)

        await ctx.send(embed=embed)


    @commands.command(name="kiss", aliases=["beijar", "beijo"])
    async def kiss_comand(self, ctx, user: discord.User = None):
        

        cur.execute('''SELECT kiss FROM Photos ORDER BY RANDOM() LIMIT 1''')
        image = cur.fetchone()[0]

        if user == None:
            user = ctx.author

        embed = discord.Embed(
            description=f"<@{ctx.author.id}> beijou <@{user.id}>!",
            colour= my_colour,
            timestamp= dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        embed.set_image(url= image)
        await ctx.send(embed=embed)

    @fala_command.error
    async def fala_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Insira algo para o bot falar!")


def setup(client):
    client.add_cog(Fun(client))
