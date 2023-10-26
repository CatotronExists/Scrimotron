import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from Keys import BOT_TOKEN
import datetime

### Vars
guildID = 1165569173880049664
channel_registration = 1165569219694448681
extension_command_list = ["team_list", "register", "unregister", "start", "end"]
full_command_list = ["team_list", "register", "unregister", "start", "end"]
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
    
bot.run(BOT_TOKEN)