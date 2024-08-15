import nextcord
from nextcord.ext import commands
from Keys import BOT_TOKEN, DB, BOT_VERSION, VERSION_NAME
import traceback
import datetime
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from BotData.colors import *

# Command Lists
command_list = admin_command_list = ["registrations", "register_trio", "register_duo", "register_solo", "schedule", "help", "configure", "score", "feedback", "scrims", "team_list", "poi_list", "player_list", "give_role", "save"]
public_command_list = ["registrations", "register_trio", "register_duo", "register_solo", "help", "feedback"]

# Discord Vars
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

### Terminal Outputs
def formatOutput(output, status, guildID):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]
    if status == "Normal": print(f"| {current_time} || {CBOLD} {guildID} {CLEAR} {output}")
    elif status == "Good": print(f"{CGREEN}| {current_time} || {CBOLD} {guildID} {CLEAR} {output} {CLEAR}")
    elif status == "Error": print(f"{CRED}| {current_time} || {CBOLD} {guildID} {CLEAR} {output} {CLEAR}")
    elif status == "Warning": print(f"{CYELLOW}| {current_time} || {CBOLD} {guildID} {CLEAR} {output} {CLEAR}")

async def logAction(guildID, user, title, description, action, type, color):
    try:
        embed = nextcord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=f"{action} by @{user}")

        await bot.get_guild(guildID).get_channel(DB[str(guildID)]['Config'].find_one({'Config': {'$exists': True}})['Config'][f'{type.lower()}LogChannel']).send(embed=embed)

    except Exception as e: formatOutput(f"   Failed to log action. Error: {e}", status="Error", guildID=guildID)

async def errorResponse(error, command, interaction: nextcord.Interaction, error_traceback):
    embed = nextcord.Embed(title="**Error**", description=f"Something went wrong while running `/{command['name']}`.\nnError: {error}", color=Red)
    embed.set_footer(text="Error was automatically sent to Catotron for review")
    try: # Try to edit response message
        await interaction.response.edit_message(embed=embed, view=None)
    except: # Try to send as response
        try: await interaction.response.send_message(embed=embed)
        except: # Try to send as followup
            try: await interaction.followup.send(embed=embed)
            except: # Try to send as new ephemeral message
                try: await interaction.send(embed=embed, ephemeral=True)
                except: pass # If all else fails, do nothing
    
    formatOutput(output=f"   Something went wrong while running /{command['name']}. Error: {error}", status="Error", guildID=command['guildID'])
    embed = nextcord.Embed(title=f"**Error Report**", description=f"Error while running /{command['name']}.\nError: {error} | {error_traceback}", color=Red)
    embed.set_footer(text=f"Guild: {command['guildID']} | User: {interaction.user.name}/{command['userID']}")
    channel = await bot.get_guild(1165569173880049664).fetch_channel(1209621162284425267)
    await channel.send(embed=embed)

### Database Functions
def getAllGuilds():
    guilds = []
    for i in DB.list_database_names():
        if i == "Scrimotron" or i == "local" or i == "admin": continue
        guilds.append(int(i))
    return guilds

def getGuildConfig(guildID):
    config_data = DB[str(guildID)]['Config'].find_one({'Config': {'$exists': True}})['Config']
    return config_data

def getGuildPresets(guildID):
    preset_data = DB[str(guildID)]['Config'].find_one({'Presets': {'$exists': True}})['Presets']
    return preset_data

def getGuildData(guildID):
    guild_data = DB[str(guildID)]['GuildData'].find_one({'guildID': guildID})
    return guild_data

def getScrims(guildID):
    scrims = list(DB[str(guildID)]['Scrims'].find({}))
    return scrims

def getScrim(guildID, scrim_name):
    scrim = DB[str(guildID)]['Scrims'].find_one({'scrimName': scrim_name})
    return scrim

def getTeams(guildID, scrim_name):
    team_data = {}
    for team in DB[str(guildID)]['Scrims'].find_one({'scrimName': scrim_name})['scrimTeams']:
        key = team
        data = DB[str(guildID)]['Scrims'].find_one({'scrimName': scrim_name})['scrimTeams'][team]
        team_data[key] = data # {teamName: teamData}

    return team_data

def getTeam(guildID, scrim_name, team_name):
    team_data = DB[str(guildID)]['Scrims'].find_one({'scrimName': scrim_name})['scrimTeams'][team_name]
    return team_data

##### Startup Terminal
start_time = datetime.datetime.now()
formatOutput(f"{CBOLD} SCRIMOTRON TERMINAL {CLEAR}", status="Good", guildID="STARTUP")
formatOutput("Loading Commands...", status="Normal", guildID="STARTUP")

for command in command_list:
    try:
        bot.load_extension(f"Commands.{command}")
        formatOutput(f"    /{command} Successfully Loaded", status="Good", guildID="STARTUP")
    except Exception as e:
        formatOutput(f"    /{command} Failed to Load // Error: {e}", status="Warning", guildID="STARTUP")

formatOutput("Commands Loaded", status="Normal", guildID="STARTUP")
formatOutput("Connecting To Database...", status="Normal", guildID="STARTUP")

try:
    DB.admin.command('ping')
    formatOutput("Connected to Database", status="Good", guildID="STARTUP")
except: formatOutput("Failed to Connect to Database", status="Error", guildID="STARTUP")

formatOutput("Connecting to Discord...", status="Normal", guildID="STARTUP")

@bot.event
async def on_ready():
    startup_time = round((datetime.datetime.now() - start_time).total_seconds() * 1000)
    formatOutput(f"{bot.user.name} has connected to Discord (Took {startup_time}ms)", status="Good", guildID="STARTUP")
    # formatOutput(f"Resuming Views...", status="Normal", guildID="STARTUP")

    # from Commands.register_trio import AutomatedRegisterView
    # view_count = 1
    # success_count = deleted_messages = 0
    # messageData = list(DB.Scrimotron.SavedMessages.find({}))
    # for entry in messageData:
    #     try:
    #         # Find Message
    #         guild = bot.get_guild(entry["guildID"])
    #         channel = guild.get_channel(entry["channelID"])
    #         message = await channel.fetch_message(entry["messageID"])
    #         # Get View Data
    #         interaction = entry["interactionID"]
    #         viewType = entry["viewType"]
    #         # Resume View
    #         view = AutomatedRegisterView(interaction, type=viewType, guildID=entry["guildID"], channelID=entry["channelID"])
    #         await message.edit(view=view)
    #         formatOutput(f"   Resuming Views: {view_count}/{len(messageData)}", status="Good", guildID="RESUMER")
    #         view_count = view_count + 1
    #         success_count = success_count + 1

    #     except Exception as e:
    #         if "Unknown Message" in str(e): # i.e. Message Deleted
    #             DB.Scrimotron.SavedMessages.delete_one({"messageID": entry["messageID"]})
    #             formatOutput(f"   Resuming Views: {view_count}/{len(messageData)} | Message Deleted", status="Warning", guildID="RESUMER")
    #             deleted_messages = deleted_messages + 1
    #             view_count = view_count + 1

    #         else: formatOutput(output=f"   Something went wrong while resuming views. Error: {e} | {traceback.format_exc()}", status="Error", guildID="RESUMER")

    # formatOutput(f"Resumed {success_count}/{len(messageData)} Views", status="Good", guildID="RESUMER")
    # formatOutput(f"Deleted {deleted_messages} Messages", status="Warning", guildID="RESUMER")

    await startScheduler() # Starts Automation

    formatOutput(f"BOT VERSION {BOT_VERSION}", status="Normal", guildID="STARTUP")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"/help | Version {BOT_VERSION}"))
    formatOutput("---------------------------------", status="Normal", guildID="STARTUP")

##### Scheduler
async def registration_updater(config_data, guildID, scrim_name, type): # Edits registrations to inlclude checkin and or poi buttons
    pass
    # formatOutput(f"   Opening {type}, Less than {config_data[f'toggle{type}Time']} Hour(s) until start", status="Normal", guildID=guildID)
    # try:
    #     channels = getChannels(guildID)
    #     scrim = getScrim(guildID, scrim_name)
    #     teams = getTeams(guildID, scrim_name)

    #     from Commands.register_trio import AutomatedRegisterView
    #     for team, team_data in teams.items():
    #         messageID = team_data["messageID"]
    #         data = DB.Scrimotron.SavedMessages.find_one_and_update({"messageID": messageID}, {"$set": {"viewType": type.lower()}})

    #         interaction = data["interactionID"]
    #         message = await bot.get_channel(data['channelID']).fetch_message(messageID)
    #         await message.edit(view=AutomatedRegisterView(interaction, type.lower(), guildID=guildID, channelID=scrim["scrimConfiguration"]["registrationChannel"]))

    #     message = splitMessage(getMessages(guildID)[f"scrim{type}"], guildID, scrim_name)
    #     channel = bot.get_channel(scrim["scrimConfiguration"]["registrationChannel"])

    #     embed = nextcord.Embed(title=message[0], description=message[1], color=White)
    #     await channel.send(embed=embed)

    #     embed = nextcord.Embed(title=f"{type}s are Open!", color=Green)
    #     embed.set_footer(text=f"🛠 Automatically Opened {config_data[f'toggle{type}Time']} hour(s) before start")

    #     await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)
    #     formatOutput(f"      Automation | {type}s Opened", status="Good", guildID=guildID)
    #     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {f"scrimConfiguration.complete.{type.lower()}": True}})

    # except Exception as e:
    #     formatOutput(output=f"   Automation | Something went wrong while opening {type.lower()}s. Error: {e} {traceback.format_exc()}", status="Error", guildID=guildID)
    #     embed = nextcord.Embed(title="Error Encountered", description=f"Error while opening {type.lower()}s.\nError: {e} {traceback.format_exc()}", color=Red)
    #     await bot.get_channel(channels["scrimLogChannel"]).send(embed=embed)

async def event_checker(): # Gets events from discord and runs automation
    pass
    # for id in DB.list_database_names(): # Get Guilds to check
    #     if id == "Scrimotron" or id == "admin" or id == "local": continue # Ignore other DBs
    #     guildID = int(id)
    #     scrims = getScrims(guildID)

    #     if scrims != []:
    #         formatOutput(f"Running Event Checker Scheduler for {bot.get_guild(guildID).name}...", status="Normal", guildID=guildID)
    #         for scrim in scrims:
    #             scrim_name = scrim["scrimName"]
    #             scrim_epoch = scrim["scrimEpoch"]
    #             current_epoch = datetime.datetime.now().timestamp()
    #             hours_until_start = (int(scrim_epoch) - int(current_epoch)) / 3600

    #             config_data = getConfigData(guildID)

    #             if hours_until_start <= -4: # If scrim started more than 4 hours ago
    #                 formatOutput(f"   Ending {scrim_name} | Scrim Started More Than 4 Hours Ago", status="Normal", guildID=guildID)

    #                 team_data = getTeams(guildID, scrim_name)
    #                 guild = bot.get_guild(guildID)

    #                 if config_data["toggleSetup"] == True: # Delete VCs
    #                     try:
    #                         for team, data in team_data.items():
    #                             vc = bot.get_channel(data["teamSetup"]["channelID"])
    #                             await vc.delete()

    #                         vc_catergory = scrim["scrimConfiguration"]["IDs"]["vcCatergory"]
    #                         await guild.get_channel(vc_catergory).delete()
    #                         formatOutput(f"   Deleted VCs for {scrim_name}", status="Good", guildID=guildID)

    #                     except Exception as e:
    #                         formatOutput(f"   Failed to delete VCs for {scrim_name}. Error: {e} {traceback.format_exc()}", status="Error", guildID=guildID)
    #                         await logAction(guildID, "AUTOMATED ACTION", f"Failed to delete VCs. Error: {e}", "Error")

    #                 try: # Delete registrations
    #                     for team, data in team_data.items():
    #                         messageID = data["messageID"]
    #                         message = await bot.get_channel(scrim["scrimConfiguration"]["registrationChannel"]).fetch_message(messageID)
    #                         await message.delete()

    #                     formatOutput(f"   Deleted Registrations for {scrim_name}", status="Good", guildID=guildID)

    #                 except Exception as e:
    #                     formatOutput(f"   Failed to delete Registrations for {scrim_name}. Error: {e} {traceback.format_exc()}", status="Error", guildID=guildID)
    #                     await logAction(guildID, "AUTOMATED ACTION", f"Failed to delete Registrations. Error: {e}", "Error")

    #                 try: # Delete team data
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimTeams": {}}})
    #                     formatOutput(f"   Deleted Team Data for {scrim_name}", status="Good", guildID=guildID)

    #                 except Exception as e:
    #                     formatOutput(f"   Failed to delete Team Data for {scrim_name}. Error: {e} {traceback.format_exc()}", status="Error", guildID=guildID)
    #                     await logAction(guildID, "AUTOMATED ACTION", f"Failed to delete Team Data. Error: {e}", "Error")

    #                 if scrim['scrimConfiguration']['interval']['repeating'] == True: # if set to repeat, reschedule
    #                     formatOutput(f"   {scrim_name} is Repeating", status="Normal", guildID=guildID)
    #                     if scrim['scrimConfiguration']['interval']['interval'] == "Daily": next_interval = 86400
    #                     elif scrim['scrimConfiguration']['interval']['interval'] == "Weekly": next_interval = 604800
    #                     elif scrim['scrimConfiguration']['interval']['interval'] == "Fortnightly": next_interval = 1209600
    #                     elif scrim['scrimConfiguration']['interval']['interval'] == "Monthly": next_interval = 2419200
    #                     new_epoch = scrim_epoch + next_interval
    #                     dateandtime = datetime.datetime.fromtimestamp(int(new_epoch))
    #                     discord_time = dateandtime.astimezone(datetime.timezone.utc)

    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimEpoch": new_epoch}})
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.interval.next": new_epoch + next_interval}})

    #                     await guild.get_scheduled_event(scrim['scrimConfiguration']['IDs']['discordEvent']).delete()
    #                     event = await guild.create_scheduled_event(
    #                         name=scrim_name,
    #                         description="Scrim Scheduled by Scrimotron",
    #                         entity_type=nextcord.ScheduledEventEntityType.external,
    #                         metadata=nextcord.EntityMetadata(location=guild.name),
    #                         start_time=discord_time,
    #                         end_time=discord_time + datetime.timedelta(hours=4),
    #                         privacy_level=nextcord.ScheduledEventPrivacyLevel.guild_only,
    #                         reason="Scrim Scheduled by Scrimotron"
    #                     )

    #                     messages = getMessages(guild.id)
    #                     message = splitMessage(messages["scrimRegistration"], guild.id, scrim_name)

    #                     channel = guild.get_channel(scrim['scrimConfiguration']['registrationChannel'])
    #                     embed = nextcord.Embed(title=message[0], description=message[1], color=White)
    #                     await channel.send(embed=embed)
    #                     await bot.get_channel

    #                     formatOutput(f"   {scrim_name} has been rescheduled", status="Good", guildID=guildID)
    #                     await logAction(guildID, "AUTOMATED ACTION", f"Rescheduled {scrim_name}", "Good")

    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.open.checkin": False}})
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.open.poi": False}})
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.complete.poi": False}})
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.complete.checkin": False}})
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.complete.setup": False}})
    #                     DB[str(guildID)]["ScrimData"].find_one_and_update({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.IDs.discordEvent": event.id}})

    #                     messages = getMessages(guildID)
    #                     message = splitMessage(messages["scrimRegistration"], guildID, scrim_name)

    #                     channel = bot.get_channel(scrim["scrimConfiguration"]["registrationChannel"])
    #                     embed = nextcord.Embed(title=message[0], description=message[1], color=White)
    #                     await channel.send(embed=embed)

    #                 else: # if not repeating, delete
    #                     await guild.get_scheduled_event(scrim['scrimConfiguration']['IDs']['discordEvent']).delete()
    #                     DB[str(guildID)]["ScrimData"].delete_one({"scrimName": scrim_name})
    #                     await logAction(guildID, "AUTOMATED ACTION", f"Ended {scrim_name}", "Good")

    #                 formatOutput(f"   {scrim_name} has Ended", status="Good", guildID=guildID)

    #             else: # Not started more than 4 hours ago -> Check for automation
    #                 automated_actions = ["toggleCheckin", "toggleSetup", "togglePoi"]
    #                 for action in automated_actions:
    #                     if action == "toggleCheckin": short = "checkin"
    #                     if action == "toggleSetup": short = "setup"
    #                     if action == "togglePoi": short = "poi"

    #                     if config_data[action] == True: # If enabled
    #                         if scrim["scrimConfiguration"]["complete"][short] == False: # If not already completed
    #                             if hours_until_start < config_data[f"{action}Time"] and config_data[action] == True: # If time to run
    #                                 if action == "toggleCheckin" or action == "togglePoi": await registration_updater(config_data, guildID, scrim_name, type=short.capitalize())
    #                                 #if action == "toggleSetup": setup_handler(config_data, guildID, scrim_name)

    #     else:
    #         formatOutput(f"   No Scheduled Scrims Found for {guildID}", status="Warning", guildID=guildID)

async def global_messager():
    formatOutput("Running Global Messager Scheduler...", status="Normal", guildID="BACKGROUND TASK")
    messages = DB["Scrimotron"]["ScheduledMessages"].find_one({"title": {"$exists": True}})
    if messages != None:
        description_parts = messages["message"].split('{}')
        description = '\n'.join(description_parts)

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
    try:
        formatOutput("Starting Scheduler...", status="Normal", guildID="STARTUP")
        scheduler = AsyncIOScheduler()
        scheduler.add_job(event_checker, 'cron', minute=0, misfire_grace_time=600) # At xx:00
        scheduler.add_job(global_messager, 'cron', minute='*/1', misfire_grace_time=30) # Every minute
        scheduler.start()
        formatOutput("Scheduler Started", status="Good", guildID="STARTUP")

    except Exception as e:
        formatOutput(f"Something went wrong while starting scheduler. Error: {e} | {traceback.format_exc()}", status="Error", guildID="STARTUP")

@bot.event
async def on_guild_join(guild):
    try:
        formatOutput(f"Joined {guild.name} ({guild.id})", status="Good", guildID=f"{CBOLD} JOINED GUILD {CLEAR}")
        embed = nextcord.Embed(title="Scrimotron has Arrived", description=f"Ready to Supercharge and automate your scrims? Run `/configure`! and customise the bot to your needs!\n\nOpen Source Apex Scrim Bot.\nhttps://github.com/CatotronExists/Scrimotron", color=White)
        embed.set_footer(text=f"Created by @Catotron | v{BOT_VERSION} {VERSION_NAME}")
        await guild.system_channel.send(embed=embed)

        if str(guild.id) in DB.list_database_names(): # Check for existing DB
            formatOutput(f"   {guild.name} already has a database", status="Normal", guildID=f"{CBOLD} ON GUILD JOIN {CLEAR}")
            return

        default_config = DB["Scrimotron"]["GlobalData"].find_one({"defaultConfig": {"$exists": True}}) # Get default config

        keys_to_replace = {"defaultMessages": "messages", "defaultConfig": "config", "defaultChannels": "channels", "defaultPresets": "presets"} # Keys to replace

        for old_key in keys_to_replace: # Format config
            if old_key in default_config:
                default_config[keys_to_replace[old_key]] = default_config.pop(old_key)

        # Create Database
        DB[str(guild.id)]["Main"].insert_one({
            "guildID": guild.id,
            "guildName": guild.name,
            "botJoinDate": date.today().strftime('%d/%m/%Y')})

        DB[str(guild.id)]["Config"].insert_one(default_config) # Insert default config

    except Exception as e:
        formatOutput(output=f"   Something went wrong while joining {guild.name}. Error: {e} | {traceback.format_exc()}", status="Error", guildID=f"{CBOLD} ON GUILD JOIN {CLEAR}")

        embed = nextcord.Embed(title="**Error Encountered**", description=f"There was an issue when joining this server, Catotron has been notifed and this should be fixed soon!", color=Red)
        await guild.system_channel.send(embed=embed)

bot.run(BOT_TOKEN)