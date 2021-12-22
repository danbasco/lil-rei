from os import name
from imports import *

class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

   
   
    @commands.command(name="help", aliases=["h", "ajuda"])
    async def help_command(self, ctx):
        
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "✉"
        
        embed = discord.Embed(
            title="Suporte da Lil Rei",
            description="Já conhece a Lil Rei? Um bot de diversão, música, economia, moderação e muito mais! Um bot completo para o seu servidor!\n\nAinda não me tem adicionada no seu servidor? Então clique [aqui](https://discord.com/api/oauth2/authorize?client_id=880584198358966303&permissions=8&scope=bot%20applications.commands) para me adicionar no seu servidor! Aproveite as melhores funções exclusivas que vou proporcionar!",
            colour= my_colour,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        embed.add_field(name="Nosso Site", value="Em breve!", inline=False)
        embed.add_field(name="Servidor de suporte", value="https://discord.gg/NMHTmXrbFD", inline=False)
        embed.add_field(name="Comandos", value="Reaja no emoji ✉ para receber uma lista de todos os comandos!")
        

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✉")
        

        try:    
            reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            ...
        else:
            embed2 = discord.Embed(
                title="Lista de comandos",
                description="Todos os comandos atuais da Lil Rei! prefixo padrão: `rei!`\n\n",
                colour= my_colour,
                timestamp = dt.datetime.utcnow()
            )
            embed2.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
            embed2.add_field(name="__MÚSICA:__", value="**rei!play**: toca uma música, pode ser link ou nome\n**rei!pause**: Pausa a música que estiver tocando\n**rei!resume:** Volta a tocar a música parada\n\n**rei!back:** Volta uma música na lista\n**rei!skip**: Avança uma música\n**rei!stop**: Para de tocar as músicas\n**rei!clear**: Para de tocar as músicas\n\n**rei!join**: Conecta no canal de voz\n**rei!leave**: Desconecta do canal de voz\n\n**rei!queue:** Mostra as próximas 10 músicas\n**rei!nowplaying**: Mostra a música atual\n\n**rei!shufle:** Músicas aleatórias da lista\n**reI!loop**: Ativa o looping da lista, ou da música\n\n**rei!quicksearch:** Ativa a busca rápida\n\n\nㅤ", inline=False)
            embed2.add_field(name="__MODERAÇÃO:__", value="**rei!ban**: Bane um usuário especifico\n**rei!unban**: Remove o ban do usuário\n**rei!kick**: Expulsa um usuário\n**rei!mute**: Silencia um usuário\n\n**rei!lock**: Bloqueia um canal de enviar mensagens\n**rei!purge**: Apaga uma quantidade de mensagens\n **rei!nuke**: Limpa um canal por completo\n\n**rei!avatar**: Mostra a foto de um usuário\n**rei!invite**: Adicione a Lil Rei no seu servidor\n**rei!prefix**: Muda o prefixo do bot no seu servidor\n\n\nㅤ", inline=False)
            embed2.add_field(name="__DIVERSÃO:__", value="**rei!fala**: Repete a mensagem enviada pelo usuário\n**rei!randomrei:** Envia uma imagem aleatória da Rei\n\n\nㅤ", inline=False)
            embed2.add_field(name="__Em Breve...__", value="Novidades em breve! Mais comandos de diversão, moderação e um sistema único de economia! Para ficar dentro das novidades, entre no nosso [servidor](https://discord.gg/NMHTmXrbFD)!\nㅤ")
            
            await ctx.author.send(embed=embed2)
            
            await msg.delete()
            await ctx.send("Mensagem enviada! Verifique suas DM para ver o comando!")
            
            
        
        


def setup(client):
    client.add_cog(HelpCommand(client))