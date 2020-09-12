import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime

client = commands.Bot(command_prefix='!')

types = ["nef", "ony", "rend", "zg"]
secondary = ["head", "head", "head", "heart"]
availability = [True, True, True, True]
reservers = ["","","",""]
timers = ["","","",""]
ampm = ["","","",""]
h = open("/home/ubuntu/dropbot/cogs/timers.txt", "w")
h.close()

@client.event
async def on_ready():
    client.load_extension(f'cogs.timer')


def isTime(arg):
    if len(arg) == 5 and arg[2] == ":":
        try:
            int(arg[0]+arg[1])
        except:
            return(False)
        try:
            int(arg[3]+arg[4])
        except:
            return(False)
        return(True)
    elif len(arg) == 4 and arg[1] == ":":
        try:
            int(arg[0])
        except:
            return(False)
        try:
            int(arg[2]+arg[3])
        except:
            return(False)
        return(True)
    else:
        return(False)
            

#timermessage = ""
def refreshMessage():
    timermessage = ""
    timermessage += "```diff\n"
    for i in range(len(availability)):
        if availability[i] == False:
            timermessage += "+ {0} {1} -> {2} {3} [{4}]\n".format(types[i].title(), secondary[i], timers[i], ampm[i], reservers[i])
        else:
            timermessage += "- {0} {1} -> {2} {3} [Not Reserved]\n".format(types[i].title(), secondary[i], timers[i], ampm[i])
    timermessage += "```"
    return(timermessage)

def refreshAvail():
    g = open("/home/ubuntu/dropbot/cogs/timers.txt", "r")
    for i in range(4):
        line = g.readline()
        if line == "\n":
            availability[i] = True
            ampm[i] = ""
            timers[i] = ""
            reservers[i] = ""
    g.close()
    

def writeFile():
    f = open("/home/ubuntu/dropbot/cogs/timers.txt", "w")
    for i in range(len(timers)):
        if ampm[i] == "AM":
            f.write(timers[i] + "\n")
        elif len(timers[i]) == 5:
            realtime = ""
            realtime += str(int(timers[i][0]+timers[i][1]) + 12)
            realtime += ":"
            realtime += timers[i][3]+timers[i][4]
            if realtime[0]+realtime[1] == "24":
                realrealtime = ""
                realrealtime += "0:"
                realrealtime += realtime[3]+realtime[4]
                f.write(realrealtime + "\n")
            else:
                f.write(realtime + "\n")
        elif len(timers[i]) == 4:
            realtime = ""
            realtime += str(int(timers[i][0]) + 12)
            realtime += ":"
            realtime += timers[i][2]+timers[i][3]
            f.write(realtime + "\n")
        else:
            f.write("\n")
    f.close()
    
@client.command()
async def dropbot(ctx):
    refreshAvail()
    message = ctx.message
    #await message.delete()
    await ctx.send(refreshMessage())

@client.command()
async def reserve(ctx, arg1, arg2, arg3):
    refreshAvail()
    message = ctx.message
    arg1 = arg1.lower()
    arg1 = arg1.title()
    if arg1.lower() in types:
        if isTime(arg2) == True:
            if arg3.lower() == "am" or arg3.lower() == "pm":
                if availability[types.index(arg1.lower())] == True:
                    await ctx.send("Reserved {0} {1} at: {2} {3}".format(arg1,secondary[types.index(arg1.lower())],arg2,arg3.upper()))
                    index = types.index(arg1.lower())
                    availability[index] = False
                    timers[index] = arg2
                    ampm[index] = arg3.upper()
                    author = "@"
                    author += message.author.name
                    author += "#"
                    author += message.author.discriminator
                    reservers[index] = author
                    writeFile()
                else:
                    await ctx.send("This buff is already reserved. Type '!dropbot' to see the timers")
                
            else:
                await ctx.send("Wrong time format")
        else:
            await ctx.send("Wrong time format")
    else:
        await ctx.send("Wrong buff type")



@client.command()
async def addtimer(ctx, arg1, arg2, arg3):
    refreshAvail()
    message = ctx.message
    arg1 = arg1.lower()
    arg1 = arg1.title()
    if arg1.lower() in types:
        if isTime(arg2) == True:
            if arg3.lower() == "am" or arg3.lower() == "pm":
                if availability[types.index(arg1.lower())] == True:
                    await ctx.send("Updated timer for {0} {1} at: {2} {3}".format(arg1,secondary[types.index(arg1.lower())],arg2,arg3.upper()))
                    index = types.index(arg1.lower())
                    timers[index] = arg2
                    ampm[index] = arg3.upper()
                    writeFile()
    
                else:
                    await ctx.send("This buff is already reserved. Type '!dropbot' to see the timers")
                
            else:
                await ctx.send("Wrong time format")
        else:
            await ctx.send("Wrong time format")
    else:
        await ctx.send("Wrong buff type")



















client.run('')
