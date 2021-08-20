'''Confirms the ownership of a registered User'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import discord
import requests
import json
import copy
import os
from mongoclient import DBClient
from packages.nitrotype import Racer

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def confirm(self, ctx, discordid):
        for role in ctx.author.roles:
            if role.id in [
              #Insert permitted role IDs here
               #SSH Administrator
                788549177545588796,
               #SSH Moderator
                788549154560671755,
               #SSH Server Support
                788549207149248562
            ]:
                bypass = True
                break
        else:
            bypass = False
        if (ctx.author.id) not in [
          #Try2Win4Glory
            505338178287173642
        ] and not bypass:
            embed = Embed('Error!', 'Lol. Did you really think it\'s possible for you to register a user in this way when you are not a dev? Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')
            return await embed.send(ctx)
        else:
            discordid = discordid.replace("!", "")
            discordid = discordid.replace("<@", "")
            discordid = discordid.replace(">", "")
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            #dbdata = await dbclient.get_array(collection, {[{'userID': str(discordid)}]})
            dbdata = await collection.find_one({"userID":str(discordid)})
            print(dbdata)
            old = copy.deepcopy(dbdata)
            async for elem in dbdata:
              elem['verified'] = 'true'
              await dbclient.update_array(collection, old, dbdata)
              embed=Embed('Success!', f'{ctx.author.mention} confirmed <@{discordid}>\'s Ownership of the NItrotype Account **{elem["NTuser"]}.')
              await embed.send(ctx)
              break
            else:
              embed = Embed('Error!', 'Doesn\'t seem like '+userid+' is registered!', 'warning')
              return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
