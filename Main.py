import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from Keys import BOT_TOKEN
import datetime
from Config import db_team_data, checkin, poi_selection, setup, db_bot_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler

### Vars
guildID = 1165569173880049664 #test server
channel_registration = 1165569219694448681 #test server - #team-rego
casterRoleID = 1166928063708282881 #caster role
channel_checkin = 1166937482009530468 #test server - #check-ins
channel_poi = 1168355452707422289 #test server #poi
channel_bot_event = 1175985885959962664 #test server #bot-event
partipantRoleID = 1168356974988111964 #participant role
extension_command_list = ["team_list", "register", "unregister", "end", "schedule", "select_poi", "help", "unregister_all"]
full_command_list = ["team_list", "register", "unregister", "end", "schedule", "select_poi", "help", "unregister_all"]
public_command_list = ["team_list", "register", "unregister", "select_poi", "help"]
admin_command_list = ["team_list", "register", "unregister", "end", "schedule", "select_poi", "help", "unregister_all"]
# Colors
import os
os.system("")
CLEAR = '\33[0m'
CGREEN = '\33[92m'
CBLUE = '\33[34m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CBEIGE = '\33[36m'
CBOLD = '\033[1m'

### Format Terminal
def formatOutput(output, status):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]
    if status == "Normal": print("| "+str(current_time)+" || "+output)
    elif status == "Good": print(CGREEN +"| "+str(current_time)+" || "+output+ CLEAR)
    elif status == "Error": print(CRED +"| "+str(current_time)+" || "+output+ CLEAR)
    elif status == "Warning": print(CYELLOW +"| "+str(current_time)+" || "+output+ CLEAR)

### Error Handler
class error_view(nextcord.ui.View):
    def __init__(self, error, command, interaction: Interaction):
        super().__init__(timeout=None)
        self.error = error
        self.command = command

    @nextcord.ui.button(label="Alert Catotron!", style=nextcord.ButtonStyle.blurple, custom_id="report_error", emoji="🚨")
    async def alert_catotron(self, button: nextcord.ui.Button, interaction: Interaction):
        user = interaction.user.name
        await interaction.response.send_message(content="Alerting Catotron...", ephemeral=True)
        try: await interaction.guild.get_member(515470819804184577).send(f"📢 Error Report from: {user}\nError: {self.error}\nError occured when running **/{self.command}**")
        except Exception as e: await interaction.edit_original_message(content=f"Something went wrong while alerting Catotron. Please contact him directly, Error: {e}.", view=None)
        await interaction.followup.send(content="Error has been sent to Catotron!", ephemeral=True)

    @nextcord.ui.button(label="Close", style=nextcord.ButtonStyle.red, custom_id="close_error", emoji="🗑")
    async def close(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.edit_message(view=None)

async def errorResponse(error, command, interaction: Interaction):
    try: await interaction.edit_original_message(content=f"Something went wrong while running /{command}. Did you mistype an entry or not follow the format?\nError: {error}", view=error_view(error, command, interaction=interaction))
    except: await interaction.response.send_message(content=f"Something went wrong while running /{command}. Did you mistype an entry or not follow the format?\nError: {error}", ephemeral=True)
    formatOutput(output=f"   Something went wrong while running /{command}. Error: {error}", status="Error")

### Discord Setup
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

formatOutput("UNITEDOCE BOT TERMINAL", status="Good")
formatOutput("Starting up Bot", status="Normal")
formatOutput("Loading Extensions...", status="Normal")
for i in extension_command_list:
    try: 
        bot.load_extension("Commands."+i)
        formatOutput(output="    /"+i+" Successfully Loaded", status="Good")
    except Exception as e: 
        formatOutput(output="    /"+i+" Failed to Load // Error: "+str(e), status="Warning")
formatOutput("Loading Bot Settings...", status="Normal")
formatOutput("Loading Database...", status="Normal")
formatOutput("Loading Commands...", status="Normal")
formatOutput("Starting Scheduler...", status="Normal")
formatOutput("Connecting to Discord...", status="Normal")

### Scheduler
async def event_finder():
    formatOutput("Running Event Check Scheduler...", status="Normal")
    events = bot.get_guild(guildID).scheduled_events
    if not events:
        formatOutput("   No Scheduled Events Found", status="Normal")
    else:
        for event in events:
            formatOutput(f"   Found Scheduled Event: {event.name}", status="Good")
            if event.start_time:
                time_until_start = event.start_time - datetime.datetime.now(datetime.timezone.utc)
                hours_until_start = time_until_start.total_seconds() / 3600
                data = db_bot_data.find_one({"setup": {"$exists": True}})
                if hours_until_start < checkin: # Checkins open 1 hour before event
                    try:
                        if data["checkin"] == 'no':
                            formatOutput(f"   Opening Checkins, Less than 1 Hour until start", status="Good")
                            team_data = list(db_team_data.find())
                            for i in team_data:
                                await bot.get_channel(channel_checkin).send(content=f"**{i['team_name']}**\n*Captain:* <@{i['captain']}>")
                            embed = nextcord.Embed(title="Checkins are Open!", color=0x000)
                            embed.set_footer(text=f"🛠 Automatically Opened {checkin} hour before start")
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            db_bot_data.update_one({"checkin": {"$exists": True}}, {"$set":{"checkin": 'yes'}})
                            formatOutput(f"      Automation | Checkins Opened", status="Good")
                    except Exception as e:
                        formatOutput(output=f"   Automation | Something went wrong while opening checkins. Error: {e}", status="Error")
                        embed = nextcord.Embed(title="Error Encountered", description=f"Error while opening checkins.\nError: {e}", color=0xFF0000)
                        await bot.get_channel(channel_bot_event).send(embed=embed)
                if hours_until_start < setup: # Setup starts 1 hour before event
                    if data["setup"] == 'no':
                        formatOutput(f"   Opening Setup, Less than 1 Hour until start", status="Good")
                        try: # build embed
                            error = False
                            started_at = datetime.datetime.utcnow()
                            teams_processed = 0
                            team_data = list(db_team_data.find())
                            embed = nextcord.Embed(title="UnitedOCE is starting!", color=0x000)
                            embed.add_field(name="Prepairing", value=f"0%", inline=True)
                            embed.add_field(name="Fetching Teams", value=f"0/{len(team_data)}", inline=True)
                            embed.add_field(name="Building Roles", value=f"0/{len(team_data)}", inline=True)
                            embed.add_field(name="Giving Roles", value=f"0/{len(team_data)}", inline=True)
                            embed.add_field(name="Creating VCs", value=f"0/{len(team_data)}", inline=True)
                            embed.add_field(name="Assigning VCs", value=f"0/{len(team_data)}", inline=True)
                            embed.set_footer(text=f"🛠 Automatically Opened {setup} hours before start")
                            message = await bot.get_channel(channel_bot_event).send(embed=embed)
                            messageID = message.id
                            message = await bot.get_channel(channel_bot_event).fetch_message(messageID)
                        except Exception as e:
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            error = True

                        try: # Make Catergory
                            catergory = await bot.get_guild(guildID).create_category_channel(name="Team VCs", overwrites={bot.get_guild(guildID).default_role: nextcord.PermissionOverwrite(view_channel=False), bot.get_guild(guildID).me: nextcord.PermissionOverwrite(view_channel=True)})
                            try: db_bot_data.delete_one({"vc_catergory": {"$exists": True}})
                            except: pass
                            db_bot_data.insert_one({"vc_catergory": catergory.id})

                            embed.set_field_at(0, name="Prepairing", value=f"**DONE**", inline=True)
                            await message.edit(embed=embed)
                        except Exception as e:
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed.set_field_at(0, name="Prepairing", value=f"**FAILED**", inline=True)
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            error = True

                        try: # Get teams
                            team_data = list(db_team_data.find())
                            embed.set_field_at(1, name="Fetching Teams", value=f"**DONE**", inline=True)
                            await message.edit(embed=embed)
                        except Exception as e:
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed.set_field_at(1, name="Fetching Teams", value=f"**FAILED**", inline=True)
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            error = True

                        try: # Make Roles
                            for i in team_data:
                                team_name = i["team_name"]
                                role = await bot.get_guild(guildID).create_role(name=team_name, mentionable=True)
                                embed.set_field_at(2, name="Building Roles", value=f"{teams_processed}/{len(team_data)}", inline=True)
                                await message.edit(embed=embed)

                                db_team_data.update_one(
                                    {"team_name": team_name}, 
                                    {"$set": {"setup.roleID": role.id}})

                                teams_processed += 1

                            embed.set_field_at(2, name="Building Roles", value=f"**DONE**", inline=True)
                            await message.edit(embed=embed)
                        except Exception as e:
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed.set_field_at(2, name="Building Roles", value=f"**FAILED**", inline=True)
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            error = True

                        try: # Assign Roles
                            teams_processed = 0
                            for i in team_data:
                                team_name = i["team_name"]
                                captain = i["captain"]
                                player2 = i["player2"]
                                player3 = i["player3"]
                                sub1 = i["sub1"]
                                sub2 = i["sub2"] 
                                role1 = bot.get_guild(guildID).get_role(db_team_data.find_one({"team_name": team_name})["setup"]["roleID"])
                                await bot.get_guild(guildID).get_member(captain).add_roles(role1)
                                await bot.get_guild(guildID).get_member(player2).add_roles(role1)
                                await bot.get_guild(guildID).get_member(player3).add_roles(role1)
                                if sub1 != "N/A": await bot.get_guild(guildID).get_member(sub1).add_roles(role1)
                                if sub2 != "N/A": await bot.get_guild(guildID).get_member(sub2).add_roles(role1)

                                embed.set_field_at(3, name="Giving Roles", value=f"{teams_processed}/{len(team_data)}", inline=True)
                                await message.edit(embed=embed)
                                teams_processed += 1

                            embed.set_field_at(3, name="Giving Roles", value=f"**DONE**", inline=True)
                            await message.edit(embed=embed)
                        except Exception as e: 
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed.set_field_at(3, name="Giving Roles", value=f"**FAILED**", inline=True)
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            error = True

                        try: # Make Voice Channels
                            teams_processed = 0
                            catergory_vc = db_bot_data.find_one({"vc_catergory": {"$exists": True}})["vc_catergory"]
                            for i in team_data:
                                team_name = i["team_name"]
                                vc = await bot.get_guild(guildID).create_voice_channel(name=team_name, category=bot.get_guild(guildID).get_channel(catergory_vc))
                                embed.set_field_at(4, name="Creating VCs", value=f"{teams_processed}/{len(team_data)}", inline=True)
                                await message.edit(embed=embed)

                                db_team_data.update_one(
                                    {"team_name": team_name}, 
                                    {"$set": {"setup.channelID": vc.id}})
                                teams_processed += 1

                            embed.set_field_at(4, name="Creating VCs", value=f"**DONE**", inline=True)
                            await message.edit(embed=embed)
                        except Exception as e: 
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed.set_field_at(4, name="Creating VCs", value=f"**FAILED**", inline=True)
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)                            
                            error = True

                        try: # Assign VCs
                            team_data = list(db_team_data.find())
                            teams_processed = 0
                            for i in team_data:
                                team_name = i["team_name"]
                                vc_id = i["setup"]["channelID"]
                                vc = bot.get_guild(guildID).get_channel(vc_id)
                                # get role and give to team members
                                role = bot.get_guild(guildID).get_role(i["setup"]["roleID"])
                                casterRole = bot.get_guild(guildID).get_role(casterRoleID)
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
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed.set_field_at(5, name="Assigning VCs", value=f"**FAILED**", inline=True)
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            error = True
        
                    if error == False:
                        try: # add time taken
                            time_taken = datetime.datetime.strftime(datetime.datetime(1, 1, 1) + (datetime.datetime.utcnow() - started_at), "%M:%S")
                            embed.set_footer(text=f"Took {time_taken} to complete")
                            embed.title = "UnitedOCE has Started!"
                            await message.edit(embed=embed)
                            db_bot_data.update_one({"setup": {"$exists": True}}, {"$set":{"setup": 'yes'}})
                            formatOutput(f"      Automation | Setup Completed", status="Good")
                        except Exception as e:
                            formatOutput(output=f"   Automation | Something went wrong while running setup. Error: {e}", status="Error")
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while running setup.\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                if hours_until_start < poi_selection: # POI Selections open 3 days before event
                    if data["poi"] == 'no':
                        try:
                            formatOutput(f"   Opening POI Selections, Less than 3 Days until start", status="Good")
                            maps = db_bot_data.find_one({"maps": {"$exists": True}})
                            map1 = maps["maps"]["map1"]
                            map2 = maps["maps"]["map2"]
                            embed = nextcord.Embed(title="POI Selections are Open!", description=f"Select a POI for {map1} & {map2} using /select_poi", color=0x000)
                            await bot.get_channel(channel_poi).send(embed=embed)
                            embed = nextcord.Embed(title="POI Selections are Open!", color=0x000)
                            embed.set_footer(text=f"🛠 Automatically Opened {poi_selection} hours before start")
                            await bot.get_channel(channel_bot_event).send(embed=embed)
                            db_bot_data.update_one({"poi": {"$exists": True}}, {"$set":{"poi": 'yes'}})
                            formatOutput(f"      Automation | POI Selections Opened", status="Good")
                        except Exception as e:
                            formatOutput(output=f"   Automation | Something went wrong while opening POI selection. Error: {e}", status="Error")
                            embed = nextcord.Embed(title="Error Encountered", description=f"Error while opening POI selection\nError: {e}", color=0xFF0000)
                            await bot.get_channel(channel_bot_event).send(embed=embed)

async def startScheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(event_finder, 'cron', minute=0)
    scheduler.start()

@bot.event
async def on_ready():
    formatOutput(f"{bot.user.name} has connected to Discord & Ready!", status="Good")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="UnitedOCE"))
    await startScheduler()

bot.run(BOT_TOKEN)