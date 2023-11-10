import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from Keys import BOT_TOKEN
import datetime
from Config import db_team_data

### Vars
guildID = 1165569173880049664 #test server
channel_registration = 1165569219694448681 #test server - #team-rego
casterRoleID = 1166928063708282881 #caster role
channel_checkin = 1166937482009530468 #test server - #check-ins
channel_poi = 1168355452707422289 #test server #poi
partipantRoleID = 1168356974988111964 #participant role
extension_command_list = ["team_list", "register", "unregister", "start", "end", "check_in", "schedule", "open_poi", "select_poi", "help", "unregister_all"]
full_command_list = ["team_list", "register", "unregister", "start", "end", "check_in", "schedule", "open_poi", "select_poi", "help", "unregister_all"]
public_command_list = ["team_list", "register", "unregister", "check_in", "select_poi", "help"]
admin_command_list = ["team_list", "register", "unregister", "start", "end", "check_in", "schedule", "open_poi", "select_poi", "help", "unregister_all"]
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

print("UNITEDOCE BOT TERMINAL")
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
formatOutput("Connecting to Discord...", status="Normal")

@bot.event
async def on_ready():
    formatOutput(bot.user.name + " has connected to Discord & Ready!", status="Good")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="UnitedOCE"))
    
bot.run(BOT_TOKEN)