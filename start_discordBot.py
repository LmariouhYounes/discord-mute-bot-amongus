### Summary

# This module initalises the discord commands and waits for
# the send command module to send instructions

# -------------------------------------------------

print("[*] Loading bot...")

import asyncio
from aiohttp import web
import discord
from discord import colour
from discord.embeds import Embed #python3 -m pip install -U discord.py[voice]
from discord.ext import commands
from discord.ext.commands import check
from discord import voice_client
from discord import Role
from discord import Guild
from discord.member import Member
from modules.config import *
from datetime import datetime #We need this to set the timestamp
import random


bot = commands.Bot(command_prefix = ".", help_command=None)

@bot.command()
async def help(ctx):
    embedHelp = discord.Embed()
    embedHelp.set_author(name="Available Commands")
    embedHelp.add_field(name="`.ping`", value="Latency of the bot", inline=False)
    embedHelp.add_field(name="`.dead` / `.d`", value="Do this if you are dead, so you stay muted until you win or lose!"
                                                                              , inline=False)
    embedHelp.add_field(name="`.kill @DiscordP1 @DiscordP2`", value="Alternative to .dead "
                                                   "requires `DISCORD ADMIN` permission", inline=False)
    embedHelp.add_field(name="`.ghostmode`", value="Mute mics AND headphones for everyone between rounds except the dead (so they can talk with each other) "
                                                   "requires `DISCORD ADMIN` permission", inline=False)
    embedHelp.add_field(name="`.users` / `.u`", value="See current users in the hosts voice channel "
                                                 "require `DISCORD ADMIN` permission", inline=False)
    embedHelp.add_field(name="`.mute` / `.m`", value="Mutes everyone that is currently not dead "
                                                   "requires `DISCORD ADMIN` permission", inline=False)
    embedHelp.add_field(name="`.unmute` / `.un`", value="Unmutes everyone in your current voice channel, only the bot "
                                                   "requires `DISCORD ADMIN` permission", inline=False)
    await ctx.send(embed=embedHelp)

global ghostmode_on
ghostmode_on = False

global dead_members
dead_members = []

global killed_members
killed_members = []

global killed_Members
killed_Members=[]

global in_discussion
in_discussion = False

global no_of_members
no_of_members = 0

@bot.event
async def on_ready():
    print("[*] Bot is ready!\n\n[*] Why not join our discord if you have any issues, ideas, \nor for early access to new updates and features!\nhttps://discord.gg/PVfewrM\n\n[*] Press Control+C to exit safely")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name="Among Us"))

@bot.command(aliases=["u","U"])
async def users(ctx):
    global is_admin
    is_admin = True 
    try:
        if ctx.author.guild_permissions.administrator != True : 
            is_admin = False
    except: pass
    try:
        if ctx.author.voice:
            try:
              if(is_admin==True):
                 string = ""
                 for member in list(bot.get_channel(ctx.author.voice.channel.id).members):
                     string = string + f"- {member}\n"
                 embedUsers=discord.Embed(title=f"Users connected in `{ctx.author.voice.channel}` : \n", description=f"`{string}`" ,color=0x00b840)
                 embedUsers.timestamp = datetime.utcnow()
                 embedUsers.set_footer(text='Among Us Bot')
                 await ctx.send(embed=embedUsers)
              else:
                 await ctx.channel.send("You don't have the `Mute Members` permission.")
            except discord.errors.Forbidden:
                 await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
         await ctx.channel.send("`You must be in a voice channel first.`")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong `({e}) I'm still in testing phase. Please contact my Developper "
                               "<@!488884916596244491>")


@bot.command(aliases=["m", "stfu", "mu","M","MU"])  
async def mute(ctx): #Mute all the voice channel members typing .mute
    global ghostmode_on
    global dead_members
    global killed_members
    global killed_Members
    global in_discussion
    in_discussion = False
    global is_admin
    is_admin = True 

    try:
        if ctx.author.guild_permissions.administrator != True : #checking if the member have an admin role
            is_admin = False
    except: pass
    try:
        if ctx.author.voice:
           try:
               if(is_admin==True): #checking that the member is an admin role
                 no_of_members = 0
                 muted_members = []
                 for member in list(bot.get_channel(ctx.author.voice.channel.id).members):
                   if member.id in dead_members and member.name in killed_members and member in killed_Members and ghostmode_on:
                     await member.edit(mute = False)
                   elif member.id not in dead_members and member.name not in killed_members and member not in killed_Members and ghostmode_on:
                     await member.edit(deafen = True, mute = True)
                     no_of_members += 1
                     await ctx.channel.send(f"Muted {no_of_members} user(s) in {ctx.author.voice.channel}.")
                   else:
                     await member.edit(mute = True)
                     no_of_members += 1
                     muted_members.append(member)
                 embedResult = discord.Embed(title="Mute Result :", description=f"I Muted {no_of_members} User(s) in {ctx.author.voice.channel}.", color=0x00b840)
                 embedResult.add_field(name="Muted by :", value=f"`{ctx.author}`", inline=True)
                 embedResult.timestamp = datetime.utcnow()
                 embedResult.set_footer(text='Among Us Bot')
                 await ctx.send(embed=embedResult)
                 muted_member = ""
                 i=0
                 for member in muted_members:
                  muted_member = muted_member + f"{i+1}- {member}\n"
                  i+=1
                 embedMute=discord.Embed(title="Muted Members List :",description=f"`{muted_member}`",color=0x00b840)
                 await ctx.send(embed=embedMute)               
               else:
                 await ctx.channel.send("You don't have the `Mute Members` permission.")
           except discord.errors.Forbidden:
                 await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
           await ctx.channel.send("`You must be in a voice channel first.`")

    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my Developper "
                               "<@!488884916596244491>")



@bot.command(aliases=["un","UN"])
async def unmute(ctx): #unmute all the members that have mute in voice channel
    global dead_members
    global killed_members
    global killed_Members
    global ghostmode_on

    global in_discussion
    in_discussion = True
    global is_admin
    is_admin = True 

    try:
        if ctx.author.guild_permissions.administrator != True : 
            is_admin = False
    except: pass

    try:
        if ctx.author.voice:
           try:
               if(is_admin==True):
                 no_of_members = 0
                 muted_members = []
                 for member in list(bot.get_channel(ctx.author.voice.channel.id).members):
                   if member.id in dead_members and member.name in killed_members and member in killed_Members and ghostmode_on:
                     await member.edit(mute = True)
                   elif member.id in dead_members and member.name in killed_members and member in killed_Members and ghostmode_on == False:
                     await member.edit(mute = True)
                   elif member.id not in dead_members and member.name not in killed_members and member not in killed_Members and ghostmode_on:
                      await member.edit(deafen = False, mute = False)
                   else:
                     await member.edit(mute = False)
                     no_of_members += 1
                     muted_members.append(member)
                 embedResult = discord.Embed(title="Unmute Result :", description=f"I Muted {no_of_members} User(s) in {ctx.author.voice.channel}.", color=0x00b840)
                 embedResult.add_field(name="Unmuted by :", value=f"`{ctx.author}`", inline=True)
                 embedResult.timestamp = datetime.utcnow()
                 embedResult.set_footer(text='Among Us Bot')
                 await ctx.send(embed=embedResult)
                 unmuted_member = ""
                 i=0
                 for member in muted_members:
                  unmuted_member = unmuted_member + f"{i+1}- {member}\n"
                  i+=1
                 embedUnmute=discord.Embed(title="Unmuted Members List :",description=f"`{unmuted_member}`",color=0x00b840)
                 await ctx.send(embed=embedUnmute)    
                 muted_members.clear()           
               else:
                 await ctx.channel.send("You don't have the `Mute Members` permission.")
           except discord.errors.Forbidden:
                 await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
           await ctx.channel.send("`You must be in a voice channel first.`")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my Developper "
                               "<@!488884916596244491>")

@bot.command(aliases=["c", "cl"])
async def clear(ctx):  #unmute and clear the dead
    global dead_members
    global killed_members
    global killed_Members
    global is_admin
    is_admin = True 

    try:
        if ctx.author.guild_permissions.administrator != True : 
            is_admin = False
    except: pass

    try:
        if ctx.author.voice:
           try:
               if(is_admin==True):
                 no_of_members = 0
                 muted_members = []
                 for member in list(bot.get_channel(ctx.author.voice.channel.id).members):
                    await member.edit(deafen = False, mute = False)
                    await member.edit(mute = False)
                 print(dead_members)
                 print(killed_members)
                 print(killed_Members)
                 if member.id in dead_members and member.name in killed_members and member in killed_Members:
                    no_of_members += 1
                    muted_members.append(member.name)
                    embedResult = discord.Embed(title="Clear Result :", description=f"I Cleared for :{no_of_members} User(s) in {ctx.author.voice.channel}.", color=0x00b840)
                    embedResult.add_field(name="Cleared by :", value=f"`{ctx.author}`", inline=True)
                    embedResult.timestamp = datetime.utcnow()
                    embedResult.set_footer(text='Among Us Bot')
                    await ctx.send(embed=embedResult)
                    cleared_member = ""
                    i=0
                    for member in killed_Members:
                       cleared_member = cleared_member + f"{i+1}- {member}\n"
                       i+=1
                    embedClear=discord.Embed(title="Cleared Members List :",description=f"`{cleared_member}`",color=0x00b840)
                    await ctx.send(embed=embedClear)  
                    killed_members.clear()
                    killed_Members.clear()   
                 else :          
                    embedResult = discord.Embed(title=":warning: : Warning !", description=f"Sorry `{ctx.author}`, But there is no Dead players to clear.", color=0xffa200)
                    embedResult.timestamp = datetime.utcnow()
                    embedResult.set_footer(text='Among Us Bot')
                    await ctx.send(embed=embedResult)
               else:
                    await ctx.channel.send("You don't have the `Mute Members` permission.")
           except discord.errors.Forbidden:
                 await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
           await ctx.channel.send("`You must be in a voice channel first.`")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my Developper "
                               "<@!488884916596244491>")


@bot.command(aliases=["d", "D"])
async def dead(ctx):
    global dead_members
    global killed_members
    global killed_Members
    global ghostmode_on
    global item

    if ghostmode_on:
        await ctx.author.edit(mute = False, deafen = False)
    else:
        await ctx.author.edit(mute = True)

    if ctx.author.id not in dead_members and ctx.author.name not in killed_members and ctx.author not in killed_Members:
        dead_members.append(ctx.author.id)
        killed_members.append(ctx.author.name)
        killed_Members(ctx.author)
        print(dead_members)
        print(killed_members)
        print(killed_Members)
        
        embedResult = discord.Embed(title=f"`{ctx.author}` You just Killed yourself.", description='\u200b', color=0x00b840)
        embedResult.timestamp = datetime.utcnow()
        embedResult.set_footer(text='Among Us Bot')
        await ctx.send(embed=embedResult)
    else :
        list = ["Hell", "Heaven"] # List
        item = random.choice(list) # Chooses randomly from list
        embedResult = discord.Embed(title=":warning: : Warning !", description=f"Sorry `{ctx.author}`, but you already in {item}.", color=0xffa200)
        embedResult.timestamp = datetime.utcnow()
        embedResult.set_footer(text='Among Us Bot')
        await ctx.send(embed=embedResult)

        


@bot.command(aliases=["k", "K"])
async def kill(ctx, *members: discord.Member):
    global dead_members
    global killed_members
    global killed_Members
    global ghostmode_on
    global no_of_members
    global is_admin
    is_admin = True 
    try:
        if ctx.author.guild_permissions.administrator != True : 
            is_admin = False
    except: pass
    try:
        if ctx.author.voice:
           try:
              if(is_admin==True):
                  for member in members:
                       if member not in list(bot.get_channel(ctx.author.voice.channel.id).members):
                          await ctx.send(f"User not in channel: `{member}`")
                          continue
                       try:
                           if ghostmode_on and in_discussion:
                             await member.edit(mute = True)
                             valid = True
                           if ghostmode_on and in_discussion == False:
                             await member.edit(mute = False, deafen = False)
                             valid = True
                           else:
                             await member.edit(mute = True)
                             valid = True
                       except Exception as e:
                         print(e)
                         await ctx.send(f"Invalid user: `{member}`")
                         valid = False

                       if valid:
                         if member.id not in dead_members and member.name not in killed_members:
                             no_of_members += 1
                             dead_members.append(member.id)
                             killed_members.append(member.name)  
                             killed_Members.append(member)
                             print(no_of_members)  
                             print(dead_members)
                             print(killed_members)
                             print(killed_Members)
                             if member.id!=ctx.author.id and member.name!=ctx.author.name:
                               embedResult = discord.Embed(title="Kill Result :", description=f"I Killed :{no_of_members} User(s) in {ctx.author.voice.channel}.", color=0x00b840)
                               embedResult.add_field(name="Killed by :", value=f"`{ctx.author}`", inline=True)
                               embedResult.timestamp = datetime.utcnow()
                               embedResult.set_footer(text='Among Us Bot')
                               await ctx.send(embed=embedResult)
                             else :
                               embedResult = discord.Embed(title=f"`{ctx.author}` You just suicided", description='\u200b', color=0x00b840)
                               embedResult.timestamp = datetime.utcnow()
                               embedResult.set_footer(text='Among Us Bot')
                               await ctx.send(embed=embedResult)
                             killed_member = ""
                             i=0
                             for member in killed_Members:
                                 killed_member = killed_member + f"{i+1}- {member}\n"
                                 i+=1
                             embedKill=discord.Embed(title="Killed Members List :",description=f"`{killed_member}`",color=0x00b840)
                             await ctx.send(embed=embedKill)
                         else:
                             embedResult = discord.Embed(title=":warning: : Warning !", description=f"Sorry `{ctx.author}` but `{member.name}` is already Dead.", color=0xffa200)
                             embedResult.timestamp = datetime.utcnow()
                             embedResult.set_footer(text='Among Us Bot')
                             await ctx.send(embed=embedResult)

              else:
                     await ctx.channel.send("You don't have the `Mute Members` permission.")
           except discord.errors.Forbidden:
                 await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
           await ctx.channel.send("`You must be in a voice channel first.`")

    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my Developper "
                               "<@!488884916596244491>")


@bot.command(aliases=["gm", "GM"])
async def ghostmode(ctx):
    global ghostmode_on
    global is_admin
    is_admin = True 
    try:
        if ctx.author.guild_permissions.administrator != True : 
            is_admin = False
    except: pass

    try: 
      if ctx.author.voice :
         try:
              if is_admin == True:
                  if ghostmode_on == False:
                     ghostmode_on = True
                     embedResult = discord.Embed(title=f"Ghost mode activated successfully by: `{ctx.author}`", description='\u200b', color=0x00b840)
                     embedResult.timestamp = datetime.utcnow()
                     embedResult.set_footer(text='Among Us Bot')
                     await ctx.send(embed=embedResult)
                     #await ctx.send("```[*] Ghost mode activated```")
                  else:
                     ghostmode_on = False
                     embedResult = discord.Embed(title=f"Ghost mode deactivated successfully by: `{ctx.author}`", description='\u200b', color=0x00b840)
                     embedResult.timestamp = datetime.utcnow()
                     embedResult.set_footer(text='Among Us Bot')
                     await ctx.send(embed=embedResult)
                     #await ctx.send("```[*] Ghost mode deactivated```")
              else :
                   await ctx.channel.send("You don't have the `Mute Members` permission.")
         except discord.errors.Forbidden:
             await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
      else:
           await ctx.channel.send("`You must be in a voice channel first.`")

    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my Developper "
                               "<@!488884916596244491>")

    


@bot.command()
async def ping(ctx):
    embedPing = discord.Embed()
    if(round(bot.latency * 1000)<200):
        embedPing.add_field(name=":green_circle:",value='\u200b', inline=True)
        embedPing.color=0x7dd100
    elif(round(bot.latency * 1000)>200 and round(bot.latency * 1000)<300):
        embedPing.add_field(name=":yellow_circle:",value='\u200b', inline=True)
        embedPing.color=0xfff700
    elif(round(bot.latency * 1000)>300 and round(bot.latency * 1000)<500):
        embedPing.add_field(name=":orange_circle:",value='\u200b', inline=True)
        embedPing.color=0xffa200
    else:
        embedPing.add_field(name=":red_circle:",value='\u200b', inline=True)
        embedPing.color=0xff0000
    embedPing.add_field(name="`Ping :`",value='\u200b', inline=True)
    embedPing.add_field(name=f"`{round(bot.latency * 1000)}ms`",value='\u200b', inline=True)
    await ctx.send(embed=embedPing)


async def handle_request(request):
    action = request.match_info.get('action', "nothing")
    if action == "mute":
        await mute(None)
    elif action == "unmute":
        await unmute(None)
    elif action == "clear":
        await clear(None)

    return web.Response(text=None)
    

async def run_bot():
    app = web.Application()
    app.router.add_get('/', handle_request)
    app.router.add_get('/{action}', handle_request)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '', port)
    await site.start()

    try:
        await bot.start(discord_bot_token)

    except KeyboardInterrupt:
        bot.close(),

    finally:
        await runner.cleanup()

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())

except OSError:
    print("[*] ERROR: address already in use")

except Exception as e:
    print(f"{e}\n\n[*] ERROR: invalid discord bot token\n")

except KeyboardInterrupt:
    print("\n[*] Exiting..")
