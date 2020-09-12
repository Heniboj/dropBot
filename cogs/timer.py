import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta


times = ["","","",""]
buffs = ["Nefarian head", "Onyxia head", "Rend head", "ZG heart"]

time = 0


def refreshFile():
    g = open("/home/ubuntu/dropbot/cogs/timers.txt", "w")
    for i in range(4):
        g.write(times[i] + "\n")
    g.close()
    

class timer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.index = 0
        self.checktimer.start()
        self.channel = client.get_channel(736620082960138331)

    def cog_unload(self):
        self.checktimer.cancel()

        
    @tasks.loop(seconds=60)
    async def checktimer(self): 
        f = open("/home/ubuntu/dropbot/cogs/timers.txt", "r")
        for i in range(4):
            line = f.readline()
            line = line.strip()
            times[i] = line
        f.close()
        now = datetime.now() + timedelta(hours=-4)
        now = datetime.strftime(now, "%H:%M")
        #print(now)
        #print(times)
        for i in range(4):
            if now == times[i]:
                #print("")
                await self.channel.send("Buff {0} can be dropped!".format(buffs[i]))
                times[i] = ""
                refreshFile()
                





    @checktimer.before_loop
    async def before_checktimer(self):
        #print('waiting...')
        #await self.bot.wait_until_ready()

#


def setup(client):
    client.add_cog(timer(client))
    
