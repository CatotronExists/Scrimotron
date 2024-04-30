import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from Keys import BOT_TOKEN, DB, BOT_VERSION
import traceback
import datetime
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random as randint
from BotData.colors import *
import re

# Command Lists
command_list = admin_command_list = ["team_list", "register_trio", "end", "schedule", "select_poi", "help", "unregister_all", "status", "configure", "score"]
public_command_list = ["team_list", "register_trio", "select_poi", "help"]

# Discord Vars
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

### Format Terminal
def formatOutput(output, status, guildID):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]
    if status == "Normal": print(f"| {current_time} || {CBOLD} {guildID} {CLEAR} {output}")
    elif status == "Good": print(f"{CGREEN}| {current_time} || {CBOLD} {guildID} {CLEAR} {output} {CLEAR}")
    elif status == "Error": print(f"{CRED}| {current_time} || {CBOLD} {guildID} {CLEAR} {output} {CLEAR}")
    elif status == "Warning": print(f"{CYELLOW}| {current_time} || {CBOLD} {guildID} {CLEAR} {output} {CLEAR}")

### Error Handler
async def errorResponse(error, command, interaction: Interaction, error_traceback):
    embed = nextcord.Embed(title="**Error**", description=f"Something went wrong while running `/{command}`.\nDid you mistype an entry or not follow the format?\nError: {error}", color=Red)
    embed.set_footer(text="Error was automatically sent to Catotron for review.")
    try: await interaction.edit_original_message(embed=embed)
    except: await interaction.response.send_message(embed=embed)
    formatOutput(output=f"   Something went wrong while running /{command}. Error: {error}", status="Error", guildID=interaction.guild.id)

    # SEND ERROR TO CHANNEL
    embed = nextcord.Embed(title=f"**Error Report**", description=f"Error while running /{command}.\nError: {error} {error_traceback}", color=Red)
    embed.set_footer(text=f"Guild: {interaction.guild.id} | User: {interaction.user.name}/{interaction.user.id}")
    channel = await bot.get_guild(1165569173880049664).fetch_channel(1209621162284425267)
    await channel.send(embed=embed)

### Message Splitter
def splitMessage(base, guildID):
    #scrim_info = DB[str(guildID)]["ScrimData"].find_one({"scrimInfo": {"$exists": True}})["scrimInfo"]
    channels = getChannels(guildID)

    #scrim_name = scrim_info["scrimName"]
    #scrim_epoch = scrim_info["scrimEpoch"]
    channel_register = channels["scrimRegistrationChannel"]
    channel_checkin = channels["scrimCheckinChannel"]
    channel_rules = channels["scrimRulesChannel"]
    channel_format = channels["scrimFormatChannel"]
    channel_poi = channels["scrimPoiChannel"]
    channel_bot_log = channels["scrimLogChannel"]

    parts = re.split(r'(\{.*?\})', base)
    placeholders = {
        #"{scrim_name}": scrim_name,
        "{channel_register}": f"<#{channel_register}>",
        "{channel_checkin}": f"<#{channel_checkin}>",
        "{channel_rules}": f"<#{channel_rules}>",
        "{channel_format}": f"<#{channel_format}>",
        "{channel_poi}": f"<#{channel_poi}>",
        "{channel_bot_log}": f"<#{channel_bot_log}>",
        # "{timing_short_time}": f"<t:{scrim_epoch}:t>",
        # "{timing_long_time}": f"<t:{scrim_epoch}:T>",
        # "{timing_short_date}": f"<t:{scrim_epoch}:d>",
        # "{timing_long_date}": f"<t:{scrim_epoch}:D>",
        # "{timing_full}": f"<t:{scrim_epoch}:f>",
        # "{timing_day_full}": f"<t:{scrim_epoch}:F>",
        # "{timing_countdown}": f"<t:{scrim_epoch}:R>",
        "{}": "\n"
    }

    for part in parts:
        if part in placeholders:
            parts[parts.index(part)] = placeholders[part]

    base = []
    base.append(parts[0])
    base.append(''.join(parts[1:]))
    return base

def unformatMessage(base, guildID):
    parts = list(base)
    placeholders = {
    "*": "\*",
    "`": "\`",
    }

    for i, part in enumerate(parts):
        for placeholder, replacement in placeholders.items():
            if placeholder in part:
                parts[i] = part.replace(placeholder, replacement)

    base = ''.join(parts[0:])
    return base

### Handy Functions
def getAllGuilds():
    guilds = []
    for i in DB.list_database_names():
        if i == "Scrimotron" or i == "local" or i == "admin": continue
        guilds.append(int(i))
    return guilds

def getChannels(guildID):
    channels = DB[str(guildID)]["Config"].find_one({"config": {"$exists": True}})["channels"]
    return channels

def getTeams(guildID):
    team_data = list(DB[str(guildID)]["TeamData"].find({}))
    return team_data

def getScrims(guildID):
    scrims = list(DB[str(guildID)]["ScrimData"].find({}))
    return scrims

def getScrim(name, guildID):
    scrim = DB[str(guildID)]["ScrimData"].find_one({"scrimName": name})
    return scrim

def getScrimSetup(guildID):
    scrim_setup = DB[str(guildID)]["ScrimData"].find_one({"scrimSetup": {"$exists": True}})
    return scrim_setup

def getScrimInfo(guildID):
    scrim_info = DB[str(guildID)]["ScrimData"].find_one({"scrimInfo": {"$exists": True}})["scrimInfo"]
    return scrim_info

def getConfigData(guildID):
    config_data = DB[str(guildID)]["Config"].find_one({"config": {"$exists": True}})["config"]
    return config_data

def getMessages(guildID):
    messages = DB[str(guildID)]["Config"].find_one({"messages": {"$exists": True}})["messages"]
    return messages

def getMainData(guildID):
    main_data = DB[str(guildID)]["Main"].find({})
    return main_data

def getConfigStatus(guildID):
    config_status = DB[str(guildID)]["Config"].find_one({"configureStatus": {"$exists": True}})
    return config_status

##### Discord Setup

# Startup Terminal
start_time = datetime.datetime.now()
formatOutput(f"{CBOLD} SCRIMOTRON TERMINAL {CLEAR}", status="Good", guildID="STARTUP")
formatOutput("Loading Commands...", status="Normal", guildID="STARTUP")

for i in command_list:
    try:
        bot.load_extension(f"Commands.{i}")
        formatOutput(f"    /{i} Successfully Loaded", status="Good", guildID="STARTUP")
    except Exception as e:
        formatOutput(f"    /{i} Failed to Load // Error: {e}", status="Warning", guildID="STARTUP")

formatOutput("Commands Loaded", status="Normal", guildID="STARTUP")
formatOutput(f"VERSION {BOT_VERSION}", status="Normal", guildID="STARTUP")
formatOutput("Connecting To Database...", status="Normal", guildID="STARTUP")

try:
    DB.admin.command('ping')
    formatOutput("Connected to Database", status="Good", guildID="STARTUP")
except Exception as e:
    formatOutput("Failed to Connect to Database", status="Error", guildID="STARTUP")

formatOutput("Starting up Bot...", status="Normal", guildID="STARTUP")
formatOutput("Connecting to Discord...", status="Normal", guildID="STARTUP")

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Startup Screen"))
    startup_time = round((datetime.datetime.now() - start_time).total_seconds() * 1000)
    formatOutput(f"{bot.user.name} has connected to Discord (Took {startup_time}ms)", status="Good", guildID="STARTUP")
    formatOutput(f"Resuming Views...", status="Normal", guildID="STARTUP")

    from Commands.register_trio import RegisterView
    x = 0
    deleted_messages = 0
    messageData = DB.Scrimotron.GlobalData.find_one({"savedMessages": {"$exists": True}})["savedMessages"]
    for entry in messageData:
        try: 
            formatOutput(f"   Resuming Views: {x}/{len(messageData)}", status="Normal", guildID="RESUMER")
            guild = bot.get_guild(entry["guildID"])
            channel = guild.get_channel(entry["channelID"])
            message = await channel.fetch_message(entry["messageID"])
            interaction = entry["interactionID"]
            viewType = entry["viewType"]
            if viewType == "registration": view = RegisterView(interaction)
            await message.edit(view=view)
            x = x + 1

        except Exception as e:
            if "Unknown Message" in str(e):
                DB.Scrimotron.GlobalData.update_one({"savedMessages": {"$exists": True}}, {"$pull": {"savedMessages": {"messageID": entry["messageID"]}}})
                formatOutput(f"   Resuming Views: {x}/{len(messageData)} | Message Deleted", status="Warning", guildID="RESUMER")
                deleted_messages = deleted_messages + 1

            else:
                error_traceback = traceback.format_exc()
                formatOutput(output=f"   Something went wrong while resuming views. Error: {e} {error_traceback}", status="Error", guildID="RESUMER")

    formatOutput(f"Resumed {x}/{len(messageData)} Views", status="Good", guildID="RESUMER")
    formatOutput("Starting Scheduler...", status="Normal", guildID="STARTUP")
    await startScheduler() # Starts Automation
    formatOutput("Scheduler Started", status="Good", guildID="STARTUP")
    formatOutput("---------------------------------", status="Normal", guildID="STARTUP")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Scrims 24/7"))

##### Scheduler
async def checkin_handler(config_data, guildID): # Runs checkin automation
    channels = getChannels(guildID)
    try:
        formatOutput(f"   Opening Checkins, Less than {config_data['toggleCheckinTime']} Hour(s) until start", status="Normal", guildID=guildID)
        team_data = getTeams(guildID)
        message = splitMessage(DB[str(guildID)]["Config"].find_one({"config": {"$exists": True}})["messages"]["scrimCheckin"], guildID)
        #^^ Splits into title and adds formatting

        embed = nextcord.Embed(title=message[0], description=message[1], color=Black)
        await bot.get_channel(channels["scrimCheckinChannel"]).send(embed=embed)
        for i in team_data:
            await bot.get_channel(channels["scrimCheckinChannel"]).send(content=f"**{i['teamName']}**\n*Captain:* <@{i['teamCaptain']}>")
            DB[str(guildID)]["ScrimData"].update_one({"teamName": i["teamName"]}, {"$set":{"teamStatus.check_in": False}})

        embed = nextcord.Embed(title="Checkins are Open!", color=Green)
        embed.set_footer(text=f"🛠 Automatically Opened {config_data['toggleCheckinTime']} hour(s) before start")
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        formatOutput(f"      Automation | Checkins Opened", status="Good", guildID=guildID)
        DB[str(guildID)]["ScrimData"].find_one({"scrimSetup": {"$exists": True}})["scrimSetup"]["complete"]["checkinComplete"] = True

    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while opening checkins. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while opening checkins.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)

async def setup_handler(config_data, guildID): # Runs setup automation
    channels = getChannels(guildID)
    scrim_setup = getScrimSetup(guildID)
    scrim_info = getScrimInfo(guildID)
    team_data = getTeams(guildID)
    try: # build embed
        if error == False:
            started_at = datetime.datetime.utcnow()
            teams_processed = 0
            embed = nextcord.Embed(title=f"{scrim_info['scrimName']} is starting!", color=Green)
            embed.add_field(name="Prepairing", value=f"0%", inline=True)
            embed.add_field(name="Fetching Teams", value=f"0/{len(team_data)}", inline=True)
            embed.add_field(name="Building Roles", value=f"0/{len(team_data)}", inline=True)
            embed.add_field(name="Giving Roles", value=f"0/{len(team_data)}", inline=True)
            embed.add_field(name="Creating VCs", value=f"0/{len(team_data)}", inline=True)
            embed.add_field(name="Assigning VCs", value=f"0/{len(team_data)}", inline=True)
            embed.set_footer(text=f"🛠 Automatically Opened {config_data['toggleSetupTime']} hour(s) before start")
            message = await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
            messageID = message.id
            message = await bot.get_channel(channels["scrimLogChannel"]).fetch_message(messageID)
    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        error = True

    try: # Make Catergory
        if error == False:
            catergory = await bot.get_guild(guildID).create_category_channel(name="Team VCs", overwrites={bot.get_guild(guildID).default_role: nextcord.PermissionOverwrite(view_channel=False), bot.get_guild(guildID).me: nextcord.PermissionOverwrite(view_channel=True)})
            DB[str(guildID)]["ScrimData"].update_one({"vc_catergory": {"$exists": True}}, {"$set":{"vc_catergory": catergory.id}})
            embed.set_field_at(0, name="Prepairing", value=f"**DONE**", inline=True)
            await message.edit(embed=embed)
    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed.set_field_at(0, name="Prepairing", value=f"**FAILED**", inline=True)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        error = True

    try: # Get teams
        if error == False:
            team_data = getTeams(guildID)
            embed.set_field_at(1, name="Fetching Teams", value=f"0/{len(team_data)}", inline=True)
            await message.edit(embed=embed)

    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed.set_field_at(1, name="Fetching Teams", value=f"**FAILED**", inline=True)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        error = True

    try: # Make Roles
        if error == False:
            teams_processed = 0
            for i in team_data:
                team_name = i["team_name"]
                role = await bot.get_guild(guildID).create_role(name=team_name, mentionable=True)
                embed.set_field_at(2, name="Building Roles", value=f"{teams_processed}/{len(team_data)}", inline=True)
                await message.edit(embed=embed)

                DB[str(guildID)]["ScrimData"].update_one(
                    {"teamName": team_name}, 
                    {"$set": {"teamSetup.roleID": role.id}})

                teams_processed += 1

            embed.set_field_at(2, name="Building Roles", value=f"**DONE**", inline=True)
            await message.edit(embed=embed)

    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed.set_field_at(2, name="Building Roles", value=f"**FAILED**", inline=True)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        error = True

    try: # Assign Roles
        if error == False:
            teams_processed = 0
            for i in team_data:
                team_name = i["teamName"]
                captain = i["teamCaptain"]
                player2 = i["teamPlayer2"]
                player3 = i["teamPlayer3"]
                sub1 = i["teamSub1"]
                sub2 = i["teamSub2"]
                team_role = bot.get_guild(guildID).get_role(team_data["teamSetup"]["roleID"])
                await bot.get_guild(guildID).get_member(captain).add_roles(team_role)
                await bot.get_guild(guildID).get_member(player2).add_roles(team_role)
                await bot.get_guild(guildID).get_member(player3).add_roles(team_role)
                if sub1 != "N/A": await bot.get_guild(guildID).get_member(sub1).add_roles(team_role)
                if sub2 != "N/A": await bot.get_guild(guildID).get_member(sub2).add_roles(team_role)

                embed.set_field_at(3, name="Giving Roles", value=f"{teams_processed}/{len(team_data)}", inline=True)
                await message.edit(embed=embed)
                teams_processed += 1

            embed.set_field_at(3, name="Giving Roles", value=f"**DONE**", inline=True)
            await message.edit(embed=embed)
    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed.set_field_at(3, name="Giving Roles", value=f"**FAILED**", inline=True)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        error = True

    try: # Make Voice Channels
        if error == False:
            teams_processed = 0
            catergory_vc = scrim_setup["vcCatergory"]
            for i in team_data:
                team_name = i["teamNname"]
                vc = await bot.get_guild(guildID).create_voice_channel(name=team_name, category=bot.get_guild(guildID).get_channel(catergory_vc))
                embed.set_field_at(4, name="Creating VCs", value=f"{teams_processed}/{len(team_data)}", inline=True)
                await message.edit(embed=embed)

                DB[str(guildID)]["ScrimData"].update_one(
                    {"teamName": team_name}, 
                    {"$set": {"teamSetup.channelID": vc.id}})
                teams_processed += 1

            embed.set_field_at(4, name="Creating VCs", value=f"**DONE**", inline=True)
            await message.edit(embed=embed)

    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed.set_field_at(4, name="Creating VCs", value=f"**FAILED**", inline=True)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)                            
        error = True

    try: # Assign VCs
        if error == False:
            team_data = getTeams(guildID)
            teams_processed = 0
            for i in team_data:
                team_name = i["teamName"]
                vc_id = i["teamSetup"]["channelID"]
                vc = bot.get_guild(guildID).get_channel(vc_id)
                # get role and give to team members
                role = bot.get_guild(guildID).get_role(i["teamSetup"]["roleID"])
                casterRole = bot.get_guild(guildID).get_role(scrim_setup["casterRole"])

                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = True
                overwrite.view_channel = True
                await vc.set_permissions(role, overwrite=overwrite) # allow team to join

                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = True
                overwrite.view_channel = True
                await vc.set_permissions(casterRole, overwrite=overwrite) # allow casters to join

                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = False
                await vc.set_permissions(bot.get_guild(guildID).default_role, overwrite=overwrite) # deny everyone else

                embed.set_field_at(5, name="Assigning VCs", value=f"{teams_processed}/{len(team_data)}", inline=True)
                await message.edit(embed=embed)
                teams_processed += 1
            embed.set_field_at(5, name="Assigning VCs", value=f"**DONE**", inline=True)
            await message.edit(embed=embed)

    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
        embed.set_field_at(5, name="Assigning VCs", value=f"**FAILED**", inline=True)
        embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        error = True

    if error == False:
        try:
            time_taken = datetime.datetime.strftime(datetime.datetime(1, 1, 1) + (datetime.datetime.utcnow() - started_at), "%M:%S")
            embed.set_footer(text=f"Took {time_taken} to complete")
            embed.title = f"{scrim_info['scrimName']} has Started!"
            embed.color = Green
            await message.edit(embed=embed)
            DB[str(guildID)]["ScrimData"].find_one({"scrimSetup": {"$exists": True}})["scrimSetup"]["complete"]["setupComplete"] = True
            formatOutput(f"      Automation | Setup Completed", status="Good")
        except Exception as e:
            error_traceback = traceback.format_exc()
            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e} {error_traceback}", status="Error", guildID=guildID)
            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e} {error_traceback}", color=Red)
            await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
    
    elif error == True:
        embed = nextcord.Embed(title="**SETUP FAILED**", description=f"{scrim_info['scrimName']} has Failed to Start!",color=Red)
        await message.edit(embed=embed)
        formatOutput(f"      Automation | Setup Failed", status="Error")

async def poi_handler(config_data, guildID): # Runs poi automation
    scrim_setup = getScrimSetup(guildID)
    channels = getChannels(guildID)
    try:
        formatOutput(f"   Opening POI Selections, Less than {config_data['togglePoiTime']} hour(s) until start", status="Normal", guildID=guildID)
        maps = scrim_setup["maps"]
        map1 = maps["maps"]["map1"]
        map2 = maps["maps"]["map2"]
        embed = nextcord.Embed(title="POI Selections are Open!", description=f"Select a POI for {map1} & {map2} using /select_poi", color=Black)
        await bot.get_channel(channels["scrimPoiChannel"]).send(embed=embed)
        embed = nextcord.Embed(title="POI Selections are Open!", color=Green)
        embed.set_footer(text=f"🛠 Automatically Opened {config_data['togglePoiTime']} hour(s) before start")
        await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
        DB[str(guildID)]["ScrimData"].find_one({"scrimSetup": {"$exists": True}})["scrimSetup"]["complete"]["poiComplete"] = True
        formatOutput(f"      Automation | POI Selections Opened", status="Good", guildID=guildID)
    except Exception as e:
                error_traceback = traceback.format_exc()
                formatOutput(output=f"   Automation | Something went wrong while opening POI selection. Error: {e} {error_traceback}", status="Error", guildID=guildID)
                embed = nextcord.Embed(title="Error Encountered", description=f"Error while opening POI selection\nError: {e} {error_traceback}", color=Red)
                await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
 
async def event_finder(): # Gets events from discord and runs automation
    for id in DB.list_database_names(): # Get Guilds to check
        if id == "Scrimotron" or id == "admin" or id == "local": continue
        guildID = int(id)
        formatOutput(f"Running Event Finder Scheduler for {bot.get_guild(guildID).name}...", status="Normal", guildID=guildID)
        events = bot.get_guild(guildID).scheduled_events
        if not events:
            formatOutput(f"   No Scheduled Events Found for {guildID}", status="Warning", guildID=guildID)
        else:
            for event in events: # Go through found events
                formatOutput(f"   Found Scheduled Event for {guildID}: {event.name}", status="Good", guildID=guildID)
                if event.start_time: # Get hours until event
                    time_until_start = event.start_time - datetime.datetime.now(datetime.timezone.utc)
                    hours_until_start = time_until_start.total_seconds() / 3600
                    config_data = DB[str(guildID)]["Config"].find_one({"config": {"$exists": True}}) # Get server config & check conditions
                    if hours_until_start < config_data["toggleCheckinTime"] and config_data["toggleCheckin"] == True: checkin_handler(config_data, guildID)
                    if hours_until_start < config_data["toggleSetupTime"] and config_data["toggleSetup"] == True: setup_handler(config_data, guildID)
                    if hours_until_start < config_data["togglePoiTime"] and config_data["togglePoi"] == True: poi_handler(config_data, guildID)

async def presence_updater():
    presence_list = ["Scrims 24/7", "/help", "Catotron Exist", "Your Scrims", f"Version {BOT_VERSION}"]
    formatOutput("Running Presence Updater Scheduler...", status="Normal", guildID="BACKGROUND TASK")
    try: 
        await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=randint.choice(presence_list)))
        formatOutput("   Presence Updated", status="Good", guildID="BACKGROUND TASK")
    except Exception as e:
        formatOutput(f"   Something went wrong while updating presence. Error: {e}", status="Error", guildID="BACKGROUND TASK")

async def global_messager():
    formatOutput("Running Global Messager Scheduler...", status="Normal", guildID="BACKGROUND TASK")
    messages = DB["Scrimotron"]["ScheduledMessages"].find_one({"title": {"$exists": True}})
    if messages != None:
        description_parts = messages["message"].split('{}')
        description = '\n'.join(description_parts) ### TEST

        embed = nextcord.Embed(title=messages["title"], description=description, color=messages["type"])
        embed.set_footer(text=messages["footer"])

        for guild in getAllGuilds():
            try: 
                bot_log_channel = DB[str(guild)]["Config"].find_one({"config": {"$exists": True}})["channels"]["scrimLogChannel"]
                if bot_log_channel != None:
                    await bot.get_channel(bot_log_channel).send(embed=embed)
                    formatOutput(f"   Sent Global Message to {bot.get_guild(guild).name}", status="Good", guildID=guild)
                else: formatOutput(f"   No Bot Log Channel Found for {bot.get_guild(guild).name}", status="Warning", guildID=guild)

            except Exception as e: # In case of error, skip that guild
                formatOutput(f"   Something went wrong while sending global message to {guild}. Error: {e}", status="Error", guildID=guild)
                continue

        DB["Scrimotron"]["ScheduledMessages"].delete_one({"title": {"$exists": True}})
        formatOutput("   All Global Messages Sent", status="Good", guildID="BACKGROUND TASK")

    else: formatOutput("   No Global Messages Found", status="Normal", guildID="BACKGROUND TASK")

async def startScheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(event_finder, 'cron', minute=0) # At xx:00
    scheduler.add_job(presence_updater, 'cron', minute='*/4') # Every 4 minutes
    scheduler.add_job(global_messager, 'cron', minute='*/1') # Every minute
    scheduler.start()

@bot.event
async def on_reaction_add(reaction: nextcord.Reaction, user: nextcord.User): # for Checkins
    # Find server and Channel
    guildID = reaction.message.guild.id
    channels = getChannels(guildID)
    channel_checkin = channels["scrimCheckinChannel"]

    if reaction.message.channel.id == channel_checkin:
        if user.bot == False:
            message = await reaction.message.channel.fetch_message(reaction.message.id)
            message = message.content.split("\n")
            team_data = getTeams(guildID)
            for i in team_data:
                if message[0] == f"**{i['teamName']}**":
                    if i["teamCaptain"] == user.id:
                        if message[0]== f'**{i["teamName"]}**':
                            if i["teamStatus"]["checkin"] == False:
                                DB[str(guildID)]["ScrimData"].update_one({"teamCaptain": user.id}, {"$set":{"teamStatus.checkin": True}})
                                formatOutput(output=f"   {i['teamName']} has checked in!", status="Good", guildID=guildID)
                    break

@bot.event
async def on_reaction_remove(reaction: nextcord.Reaction, user: nextcord.User): # for Checkins
    # Find server and Channel
    guildID = reaction.message.guild.id
    channels = getChannels(guildID)
    channel_checkin = channels["scrimCheckinChannel"]

    if reaction.message.channel.id == channel_checkin:
        if user.bot == False:
            message = await reaction.message.channel.fetch_message(reaction.message.id)
            message = message.content.split("\n")
            team_data = getTeams(guildID)
            for i in team_data:
                if message[0] == f"**{i['teamName']}**":
                    if i["teamCaptain"] == user.id:
                        if message[0]== f'**{i["teamName"]}**':
                            if i["teamStatus"]["checkin"] == True:
                                DB[str(guildID)]["ScrimData"].update_one({"teamCaptain": user.id}, {"$set":{"teamStatus.checkin": False}})
                                formatOutput(output=f"   {i['teamName']} has unchecked in!", status="Good", guildID=guildID)
                    break

@bot.event
async def on_guild_join(guild):
    try:
        formatOutput(f"Joined {guild.name} ({guild.id})", status="Good", guildID=f"{CBOLD} JOINED GUILD {CLEAR}")
        embed = nextcord.Embed(title="Scrimotron has Arrived", description=f"Ready to Supercharge and automate your scrims? Run `/configure`! and customise the bot to your needs!\n\nOpen Source Apex Scrim Bot.\nhttps://github.com/CatotronExists/Scrimotron", color=White)
        embed.set_footer(text=f"Created by @Catotron")
        await guild.system_channel.send(embed=embed)
        botJoinDate = date.today().strftime('%d/%m/%Y') # Get current date in DD/MM/YYYY

        if str(guild.id) in DB.list_database_names(): # Check for existing DB
            formatOutput(f"   {guild.name} already has a database", status="Normal", guildID=f"{CBOLD} ON GUILD JOIN {CLEAR}")
            return
        
        default_config = DB["Scrimotron"]["GlobalData"].find_one({"defaultConfig": {"$exists": True}}) # Get default config

        keys_to_replace = {"defaultMessages": "messages", "defaultConfig": "config", "defaultChannels": "channels"}

        for old_key in keys_to_replace: # Format config
            if old_key in default_config:
                default_config[keys_to_replace[old_key]] = default_config.pop(old_key)

        # Create Database
        DB[str(guild.id)]["Main"].insert_one({
            "guildID": guild.id,
            "guildName": guild.name,
            "botJoinDate": botJoinDate})
        
        DB[str(guild.id)]["Config"].insert_one(default_config) # Insert default config

        DB[str(guild.id)]["ScrimData"].insert_one({
            "scrimInfo": {
                "scrimName": None,
                "scrimEpoch": None},
            "scrimSetup": {
                "maps": {
                    "map1": None,
                    "map2": None},
                "poiSelectionMode": None,
                "poiSelectionOpen": None,
                "teamType": None,
                "repeating": None, # Soon
                "repeatingInterval": None, # Soon
                "vcCatergory": None,
                "casterRole": None,
                "complete": {
                    "checkinComplete": False,
                    "setupComplete": False,
                    "poiComplete": False}},
            "scrimTeams": None})
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        formatOutput(output=f"   Something went wrong while joining {guild.name}. Error: {e} {error_traceback}", status="Error", guildID=f"{CBOLD} ON GUILD JOIN {CLEAR}")
        embed = nextcord.Embed(title="**Error Encountered**", description=f"There was an issue when joining this server, Catotron has been notifed and this should be fixed soon!", color=Red)
        await guild.system_channel.send(embed=embed)

bot.run(BOT_TOKEN)