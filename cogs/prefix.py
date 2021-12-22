from imports import *


class Prefixes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix=None):

        if prefix is None:
            return await ctx.send(f"Especifique um prefixo para mudar!")
        
        prefixes = self.client.prefixes

        data = await prefixes.find(ctx.guild.id)

        if data is None or "prefix" not in data:
            data = {"_id": ctx.guild.id, "prefix":prefix}
        
        data["prefix"] = prefix

        await prefixes.upsert(data)
        await ctx.send(f"O prefixo foi atualizado para `{prefix}`")


def setup(client):
    client.add_cog(Prefixes(client))

        
