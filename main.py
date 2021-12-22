from imports import *
import motor.motor_asyncio as masyncio
import discordmongo

intents = discord.Intents.default()
intents.members = True


async def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(client.DEFAULT_PREFIX)(client, message)
    
    try:
        data = await client.prefixes.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or(client.DEFAULT_PREFIX)(client, message)
        
        return commands.when_mentioned_or(data["prefix"])(client, message)

    except:
        return commands.when_mentioned_or(client.DEFAULT_PREFIX)(client, message)

    

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, owner_id=711615552925466735, help_command=None) #CLIENT
slash = SlashCommand(client, sync_commands=True) #SLASH


client.DEFAULT_PREFIX = "rei!"

   

#STATS

async def activity():
    await client.wait_until_ready()

    status = [
        f"em {str(len(client.guilds))} servidores", "rei!help para ver os comandos!", "Em criação..."
    ]

    while not client.is_closed():
        
        stats = random.choice(status)

        activity = discord.Game(name= stats, type= 3)
        await client.change_presence(status=discord.Status.online, activity=activity)

        await asyncio.sleep(30)

client.loop.create_task(activity())


##COGS


if __name__ == "__main__":
    
    client.mongo = masyncio.AsyncIOMotorClient("mongodb+srv://danbas:lilrei2021app@myclusterrei.a2bkp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    client.db = client.mongo["databasel"]
    client.prefixes = discordmongo.Mongo(connection_url=client.db, dbname="prefix")

    for files in os.listdir("./cogs"):
        if files.endswith(".py"):
            client.load_extension(f"cogs.{files[:-3]}")
            print(f"Cog {files} carregada!")


##EVENTS


@client.event
async def on_connect():
    print(f" Connected to Discord (latency: {client.latency*1000:,.0f} ms).")


@client.event
async def on_resumed():
    print("Bot resumed.")


@client.event
async def on_disconnect():
    print("Bot disconnected.")


@client.event
async def on_ready():

    print("Bot está pronto")

@client.event
async def on_message(message):
    
    if client.user.mentioned_in(message):
        if "@" not in message.content.lower():
            return ...
        
        if ("everyone" or "here" ) in message.content.lower():
            return ...
        
        await message.channel.send(f"O meu prefixo padrão é `rei!`")
    else:
        await client.process_commands(message)


## GUILDS


@client.event
async def on_guild_join(guild):
    
    servers = str(len(client.guilds))

    activity = discord.Game(name= f"Em {servers} servidores!", type= 3)
    await client.change_presence(status=discord.Status.online, activity=activity)

    print("Status alterado com sucesso")

@client.event
async def on_guild_remove(guild):
    
    servers = str(len(client.guilds))

    activity = discord.Game(name= f"Em {servers} servidores!", type= 3)
    await client.change_presence(status=discord.Status.online, activity=activity)

    print("Status alterado com sucesso")



#ERRORS

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
            await ctx.reply("**Você não tem permissão para executar esse comando!**")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"O comando {ctx.message} não foi encontrado!")


##TOKEN

def run():
    with open("data/token.0", "r", encoding="utf-8") as f:
        TOKEN = f.read()

    client.run(TOKEN)

run()
