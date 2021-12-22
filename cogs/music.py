from discord import client
from imports import *

from enum import Enum
from togglesearch import *




URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

##CLASSES#

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoChannelConnected(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

class NoTrackFound(commands.CommandError):
    pass

class InvalidRepeatMode(commands.CommandError):
    pass

class PlayerIsAlreadyPaused(commands.CommandError):
    pass

class PlayerIsAlreadyPlaying(commands.CommandError):
    pass

class NoMoreTracks(commands.CommandError):
    pass

class NoPreviousTracks(commands.CommandError):
    pass

class RepeatMode(Enum):
    NONE = 0
    MUSIC = 1
    ALL = 2

class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None
        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def empty(self):
        self._queue.clear()
        self.position = 0

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "music":
            self.repeat_mode = RepeatMode.MUSIC
        elif mode == "queue":
            self.repeat_mode = RepeatMode.ALL
    
    

##PLAYER

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel:= getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        
        if not tracks:
            raise NoTrackFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
           
            embed = discord.Embed(
                name="**Música:**",
                description=f"**{tracks[0].title}** foi adicionada a queue!",
                colour=my_colour,
                timestamp= dt.datetime.utcnow()
            )
            embed.set_author(name="Resultados da pesquisa")
            embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)


            await ctx.send(embed=embed)
        
        
        else:
            if str(ctx.guild.id) in togglesearch:
                self.queue.add(tracks[0])
                embed = discord.Embed(
                name="**Música:**",
                description=f"**{tracks[0].title}** foi adicionada a queue!",
                colour=my_colour,
                timestamp= dt.datetime.utcnow()
                )
                embed.set_author(name="Resultados da pesquisa")
                embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)


                await ctx.send(embed=embed)
            else:
            
                if (track := await self.choose_track(ctx, tracks)) is not None:
                    self.queue.add(track)
                
                    embed = discord.Embed(
                    name="**Música:**",
                    description= f"**{track.title}** foi adicionada a queue!",
                    colour=my_colour,
                    timestamp= dt.datetime.utcnow()
                )
                embed.set_author(name="Resultados da pesquisa")
                embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)


                await ctx.send(embed=embed)
                
        if not self.is_playing:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
            r.emoji in OPTIONS.keys()
            and u == ctx.author
            and r.message.id == msg.id
            )

        embed = discord.Embed(
        title= "Escolha a música",
        description= (
            "\n".join(
                f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                for i, t in enumerate(tracks[:5])
            )
        ),
        colour= my_colour,
        timestamp= dt.datetime.utcnow()
        )
        embed.set_author(name="Resultados da pesquisa")
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout =60.0, check =_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
            await ctx.send("**Tempo Limite esgotado!**")
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]
        

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track:= self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass
    
    async def repeat_track(self):
        await self.play(self.queue.current_track)

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())


#EVENTS
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await asyncio.sleep(300)
                await self.get_player(member.guild).teardown()
    
    @wavelink.WavelinkMixin.listener()
    async def on_node(self, node):
        print(f"Wavelink node `{node.identifier} ready`")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.MUSIC:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()


    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Esse comando não pode ser usado na DM")
            return False
        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "lavalink-lilrei-2.herokuapp.com",
                "port": 80,
                "rest_uri": "http://lavalink-lilrei-2.herokuapp.com:80",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "southamerica",
                "secure": False
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

#COMMANDS

    #SKIP

    @commands.command(aliases=["s","pular"])
    async def skip(self, ctx):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)
            if not player.queue.upcoming:
                await ctx.reply("Não tem nenhuma música depois dessa para tocar!")
            else:

                await player.stop()
                await ctx.send("Pulando para a próxima música...")


    
    #BACK


    @commands.command(aliases=["anterior","b", "voltar"])
    async def back(self, ctx):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)
            
            if not player.queue.history:
                await ctx.reply("**Essa é a primeira música da lista!**")
            
            else:

                player.queue.position -= 2
                await player.stop()
                await ctx.send("Voltando uma música...")


    #SHUFFLE


    @commands.command(name="shuffle", aliases=["random, aleatorio"])
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send("Músicas aleatórias da playlist vindo!")


    #RESUME

    @commands.command(name="resume")
    async def resume_command(self, ctx):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)

            if player.is_paused:
                await player.set_pause(False)
                await ctx.send("Reproduzindo a música...")

            else:
                await ctx.send("A música já está tocando!")


    #CONNECT


    @commands.command(name="connect", aliases=["join", "conectar", "entrar"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)
            channel = await player.connect(ctx, channel)
            await ctx.send(f"Conectado no canal de voz **{channel.name}**")



    #LEAVE


    @commands.command(aliases=["sair", "desconectar"])
    async def leave(self, ctx):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)

            if not player.is_connected:
                
                await ctx.send("O bot não está em nenhum canal")
            
            else:

                await player.teardown()
                await ctx.send("Desconectado do canal")


    #PLAY


    @commands.command(aliases=["tocar", "p"])
    async def play(self, ctx, *, query: t.Optional[str]):
        
        player = self.get_player(ctx)
        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if not player.is_paused:
                raise PlayerIsAlreadyPlaying

            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Reproduzindo a música...")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))



    #PAUSE


    @commands.command(aliases=["pausa", "pausar"])
    async def pause(self, ctx):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)
            if not player.is_connected:
                raise NoVoiceChannel

            elif player.is_paused:
                raise PlayerIsAlreadyPaused

            await player.set_pause(True)
            await ctx.send("Música pausada")


    
    #STOP


    @commands.command(name="stop", aliases=["clear"])
    async def stop_command(self, ctx):
        if commands.has_role("DJ") or commands.has_permissions(administrator=True):
            player = self.get_player(ctx)
            player.queue.empty()
            await player.stop()
            await ctx.send("Música parada.")



    #QUEUE


    @commands.command(name="queue", aliases=["q"])
    async def queue_command(self, ctx, show: int = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title= "Lista",
            description= f"__Mostrando próximas {show} músicas:__",
            colour= my_colour,
            timestamp= dt.datetime.utcnow()
        )
        embed.set_author(name="Resultados de música")
        embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
        embed.add_field(name="__Tocando:__", value= player.queue.current_track.title, inline= False)
        if upcoming := player.queue.upcoming:
            embed.add_field(
            name= "Próxima música:",
            value= "\n".join(t.title for t in upcoming[:show]),
            inline= False
            )

        msg = await ctx.send(embed=embed)


    
    #LOOP



    @commands.command(aliases = ["loop"])
    async def repeat(self, ctx, mode: str):

        if mode not in ("none", "music", "queue"):
            await ctx.reply("Modo de Loop Inválido!")

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        
        if "none" in mode:
            await ctx.send("**Loop cancelado!**")
        else:
            await ctx.send(f"**Looping ativado para:** {mode}")



    
    #QUICKSEARCH


     
    @commands.command(name="quicksearch", aliases=["qc"])
    async def quicksearch_command(self, ctx):
        
        guild_id = str(ctx.guild.id)

        if guild_id in togglesearch:
            togglesearch.remove(guild_id)
            await ctx.send("**Busca rápida destivada!**")
        else:
            togglesearch.append(guild_id)
            await ctx.send("**Busca rápida ativada!**")




    #NOWPLAYING



    @commands.command(aliases=["np", "nowplaying", "playing"])
    async def tocando(self, ctx):
        
        player = self.get_player(ctx)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)             
            

        if not player.is_playing:
            raise QueueIsEmpty

        

        embed = discord.Embed(
        title="",
        colour=my_colour,
        timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Tocando:")

        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name= player.queue.current_track, value=f"Tempo: **{int(position[0])}:{round(position[1]/1000):02} - {int(length[0])}:{round(length[1]/1000):02}**", inline=False)


        await ctx.send(embed=embed)

    
    ##ERRORS
    
    
    @repeat.error
    async def repeat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                name= "Comando: Loop",
                description= "**Opções do comando:**\n\n**1-**\n -loop music (Loop da música)\n\n**2-**\n-loop queue (Loop da lista)\n\n**3-**\n-loop none (cancela o loop)",
                colour= my_colour,
                timestamp= dt.datetime.utcnow()
            )
            embed.set_author(name="Especifique um comando!")
            embed.set_footer(text= f"Solicitado por {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
            await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("**A lista de músicas está vazia!**")
        
        if isinstance(exc, NoChannelConnected):
            await ctx.reply("**O bot não está em nenhum canal**")
        
        if isinstance(exc, PlayerIsAlreadyPlaying):
            await ctx.reply("**A música já está tocando!**")
        
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.reply("O bot já está em um canal")
        
        if isinstance(exc, NoVoiceChannel):
            await ctx.reply("Nenhum canal foi encontrado!")
        
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.reply("A música já está pausada")
        
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.reply(f"O bot já está em um canal")


def setup(bot):
    bot.add_cog(Music(bot))
