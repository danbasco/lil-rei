from datetime import datetime
from inspect import Arguments
from os import name
from discord import guild, user
from discord.errors import InvalidArgument
from discord.ext.commands.core import Command
from discord.ext.commands.errors import CommandError
from imports import *


class NotInRole(commands.CommandError):
    pass

class AlreadyInRole(commands.CommandError):
    pass

class ChannelAlreadyLocked(commands.CommandError):
    pass

class ChannelAlreadyUnlocked(commands.CommandError):
    pass

class MemberNotFound(commands.CommandError):
    pass

class SelfMentioned(commands.CommandError):
    pass

class OnTop(commands.CommandError):
    pass


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client


    slash = cog_ext.cog_slash


#COMMANDS

    #PURGE

    @commands.command()
    async def purge(self, ctx, amount=None):
        
        
        if amount is None:
           return await ctx.send("Especifique uma quantidade para limpar!")
        
        try:
            int(amount)
        except:
            await ctx.send("O valor inserído é inválido!")
        else:
            if int(amount) > 1000:
                await ctx.send("O valor inserido tem que estar entre 1 e 1000!")
            else:
                await ctx.channel.purge(limit=int(amount))
                await ctx.send(f"{amount} mensagens foram deletadas!")
  
    
    
    #NUKE


    @commands.command()
    @has_permissions(administrator= True)
    async def nuke(self, ctx):

        await ctx.reply("**__Digite confirmar para deletar o canal!__**")

        channel = ctx.channel
                
        def check(message):
            return message.author == ctx.author and message.content == 'confirmar' and message.channel == channel
                
        try: 
            message = await self.client.wait_for("message", timeout=10, check=check)
    
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado!")
        else:
            await channel.clone(reason= "Nuke Channel")
            await channel.delete()


    @slash(name="nuke", description="Limpe o canal de texto por completo")
    @has_permissions(administrator= True)
    async def nuke_command(self, ctx):

        await ctx.reply("**__Digite confirmar para deletar o canal!__**")

        channel = ctx.channel
                
        def check(message):
            return message.author == ctx.author and message.content == 'confirmar' and message.channel == channel
                
        try: 
            message = await self.client.wait_for("message", timeout=10, check=check)
    
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado!")
        else:
            await channel.clone(reason= "Nuke Channel")
            await channel.delete()



    #INVITE



    @commands.command(aliases=["convite", "convidar"])
    async def invite(self, ctx):
        
        embed = discord.Embed(
            name= "Adicione a Lil Rei para o seu server!",
            description= "Clique [aqui](https://discord.com/api/oauth2/authorize?client_id=880584198358966303&permissions=8&scope=bot%20applications.commands) para adicionar a Lil Rei no seu servidor! Gostaria de entrar no nosso servidor de suporte? Então clique [aqui!](https://discord.gg/NMHTmXrbFD)",
            colour= my_colour,
            timestamp= dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        
        await ctx.send(embed=embed)


    @slash(name="invite", description= "Adicione a Lil Rei no seu server!")
    async def invite_command(self, ctx):
        
        embed = discord.Embed(
            name= "Adicione a Lil Rei para o seu server!",
            description= "Clique [aqui](https://discord.com/api/oauth2/authorize?client_id=880584198358966303&permissions=8&scope=bot%20applications.commands) para adicionar a Lil Rei no seu servidor! Em breve teremos um servidor de suporte!",
            colour= my_colour,
            timestamp= dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        
        await ctx.send(embed=embed)



    #BAN



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason = None):
        
        if user is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < user.top_role:
            raise OnTop
        
        
        embed = discord.Embed(
        title = "Ban",
        description= f"**__{user} Foi banido do servidor__**",
        colour=my_colour,
        timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        
        if reason is not None:

            embed.add_field(name="Motivo:", value=f"{reason}")
            
            await user.ban(reason=reason)
            await ctx.send(embed=embed)
            await ctx.delete()

        else:
        
            await user.ban(reason=reason)
            await ctx.send(embed=embed)
            await ctx.delete()
        

    
    @slash(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx, user: discord.Member, *, reason = None):     
        
        if user is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < user.top_role:
            raise OnTop
        
        await user.ban(reason=reason)

        embed = discord.Embed(
        title = "Ban",
        description= f"**__{user} Foi banido do servidor__**",
        colour=my_colour,
        timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        
        
        if reason is not None:

            embed.add_field(name="Motivo:", value=f"{reason}")
            
            await ctx.send(embed=embed)
            await ctx.delete()
        
        else:

            await user.ban(reason=reason)
            await ctx.send(embed=embed)
            await ctx.delete() 


    #UNBAN

    
          
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        
        banned_users = await ctx.guild.bans()

        if member.isdigit():
            await ctx.send("**__Digite o nome do usuário com a tag__!**")

        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Desbanido {user.mention}')
    
    @slash(name="unban", description="Insira Tag do usuário para desbanir")
    @commands.has_permissions(ban_members=True)
    async def unban_command(self, ctx, *, member):
        
        banned_users = await ctx.guild.bans()

        if member.isdigit():
            await ctx.send("**__Digite o nome do usuário com a tag__!**")

        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Desbanido {user.mention}')



    #AVATAR

    @commands.command()
    async def avatar(self, ctx, *, user: discord.User = None):

        if user == None:
            user = ctx.message.author
            
        embed = discord.Embed(
        title= user.display_name,
        description=f"Clique [aqui]({user.avatar_url}) para baixar a imagem",
        colour=my_colour,
        timestamp = dt.datetime.utcnow()
        )
            
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        embed.set_image(url=user.avatar_url)
            
        await ctx.send(embed=embed)


            

    @slash(name="avatar")
    async def avatar_command(self, ctx, *, user: discord.User = None):
        
        if user is None:
            user = ctx.author
               
        embed = discord.Embed(
        title= user.display_name,
        description=f"Clique [aqui]({user.avatar_url}) para baixar a imagem",
        colour=my_colour,
        timestamp = dt.datetime.utcnow()
        )
            
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        embed.set_image(url=user.avatar_url)
            
        await ctx.send(embed=embed)
    


    ##MUTE

    @commands.command(aliases=["mutar", "silenciar"])
    @commands.has_permissions(kick_members= True)
    async def mute(self, ctx, user: discord.Member):

        if user is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < user.top_role:
            raise OnTop
        
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Silenciado")

        if role in user.roles:
            raise AlreadyInRole
        
        if role not in guild.roles:
            
            await guild.create_role(name= "Silenciado")

            for channel in guild.channels:
                role = discord.utils.get(guild.roles, name="Silenciado")
                await channel.set_permissions(role, send_messages=False)
         
        else:
            ...

        await user.add_roles(role)
        embed = discord.Embed(
            title="Silenciado",
            description=f"**O usuário {user} foi silenciado por {ctx.message.author}**",
            colour=my_colour,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @slash(name="mute", description="Silencie um usuário!")
    @commands.has_permissions(kick_members= True)
    async def mute_command(self, ctx, user: discord.Member):

        if user is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < user.top_role:
            raise OnTop

        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Silenciado")

        if role in user.roles:
            raise AlreadyInRole
        
        if role not in guild.roles:
            
            await guild.create_role(name= "Silenciado")

            for channel in guild.channels:
                role = discord.utils.get(guild.roles, name="Silenciado")
                await channel.set_permissions(role, send_messages=False)
         
        else:
            ...

        await user.add_roles(role)
        embed = discord.Embed(
            title="Silenciado",
            description=f"**O usuário {user} foi silenciado!**",
            colour=my_colour,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        await ctx.send(embed=embed)


    
    #UNMUTE


    @commands.command(aliases=["desmutar", "dessilenciar"])
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):

        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Silenciado")

        if role not in user.roles:
            raise NotInRole

        await user.remove_roles(role)
        
        embed= discord.Embed(
            title="Desmutado",
            description=f"**O usuário {user} foi desmutado!**",
            colour=my_colour,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @slash(name="unmute", description="Desmute o usuário")
    @commands.has_permissions(mute_members=True)
    async def unmute_command(self, ctx, user: discord.Member):

        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Silenciado")
        
        if role not in user.roles:
            raise NotInRole
        
        await user.remove_roles(role)
        
        embed= discord.Embed(
            title="Desmutado",
            description=f"**O usuário {user} foi desmutado!**",
            colour=my_colour,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        await ctx.send(embed=embed)



    ##LOCK

    @commands.command(aliases=["bloquear"])
    @commands.has_permissions(kick_members=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        
        guild = ctx.guild

        if channel is not None:

            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == False:
                raise ChannelAlreadyLocked

            await channel.set_permissions(guild.default_role, send_messages=False)
            await ctx.send(f"**O canal {channel} foi bloqueado!** Utilize `rei!unlock` para desbloquear.")

        else:
            
            channel = ctx.message.channel
            
            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == False:
                raise ChannelAlreadyLocked

            await channel.set_permissions(guild.default_role, send_messages=False)

            await ctx.send("**Canal bloqueado!** Utilize `rei!unlock` para desbloquear.")


    @slash(name="lock", description="Bloqueia o canal")
    @commands.has_permissions(kick_members=True)
    async def lock_command(self, ctx, channel: discord.TextChannel = None):
        
        guild = ctx.guild

        if channel is not None:

            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == False:
                raise ChannelAlreadyLocked

            await channel.set_permissions(guild.default_role, send_messages=False)
            await ctx.send(f"**O canal {channel} foi bloqueado!** Utilize `rei!unlock` para desbloquear.")

        else:
            
            channel = ctx.message.channel
            
            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == False:
                raise ChannelAlreadyLocked

            await channel.set_permissions(guild.default_role, send_messages=False)

            await ctx.send("**Canal bloqueado!** Utilize `rei!unlock` para desbloquear.")

            
    ##UNLOCK

    @commands.command(alases=["desbloquear"])
    @commands.has_permissions(kick_members=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        
        guild = ctx.guild

        if channel is not None:

            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == True:
                raise ChannelAlreadyUnlocked

            await channel.set_permissions(guild.default_role, send_messages=True)
            await ctx.send(f"**O canal {channel} foi desbloqueado!**")

        else:
            
            channel = ctx.message.channel

            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == True:
                raise ChannelAlreadyUnlocked

            await channel.set_permissions(guild.default_role, send_messages=True)

            await ctx.send("**Canal desbloqueado!**")


    @slash(name= "unlock", description="Desbloqueia o canal")
    @commands.has_permissions(kick_members=True)
    async def unlock_command(self, ctx, channel: discord.TextChannel = None):
        
        guild = ctx.guild

        if channel is not None:

            overwrite = channel.overwrites_for(guild.default_role)
            if overwrite.send_messages == True:
                raise ChannelAlreadyUnlocked

            await channel.set_permissions(guild.default_role, send_messages=True)
            await ctx.send(f"**O canal {channel} foi desbloqueado!**")

        else:
            
            channel = ctx.message.channel

            overwrite = channel.overwrites_for(ctx.guild.default_role)
            if overwrite.send_messages == True:
                raise ChannelAlreadyUnlocked

            await channel.set_permissions(guild.default_role, send_messages=True)

            await ctx.send("**Canal desbloqueado!**")
        

    ##KICK


    @commands.command(aliases= ["expulsar"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        
        if member is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < member.top_role:
            raise OnTop
        
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="Kick",
            description=f"O usuário {member} foi expulso do servidor!",
            colour=my_colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        if reason is not None:
            embed.add_field(name= "Motivo:", value= reason)
            return await ctx.send(embed=embed)

        await ctx.send(embed=embed)

    @slash(name="kick", description="Expulsa um membro")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: discord.Member, reason=None):

        if member is ctx.message.author:
            raise SelfMentioned

        if ctx.author.top_role < member.top_role:
            raise OnTop
        
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="Kick",
            description=f"O usuário {member} foi expulso do servidor!",
            colour=my_colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        if reason is not None:

            embed.add_field(name= "Motivo:", value= reason)
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=embed)
        

    ##ERRORS
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):

        if isinstance(exc, AlreadyInRole):
            await ctx.reply("O usuário já está mutado!")

        if isinstance(exc, NotInRole):
            await ctx.reply("O usuário não está mutado!")

        if isinstance(exc, ChannelAlreadyLocked):
            await ctx.reply("O canal já está bloqueado! **Utilize `rei!unlock` para desbloquear!**")

        if isinstance(exc, ChannelAlreadyUnlocked):
            await ctx.reply("O canal já está desbloqueado!")

        if isinstance(exc, MemberNotFound):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")

        if isinstance(exc, SelfMentioned):
            await ctx.reply("Você não pode mencionar a si mesmo!")    
        
        if isinstance(exc, OnTop):
            await ctx.reply("Você não tem permissão para executar esse comando!")    

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Não foi possível encontrar o usuário! Verifique se foi digitado corretamente")

    

def setup(client):
    client.add_cog(Admin(client))

