import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, public_command_list, admin_command_list
from BotData.colors import *

help_descriptions = {
"registrations": {
    "warning": ":warning: *Renamed (was `/team_list`)*",
    "small_text": "Shows a full list of teams, players and subs",
    "description": "Shows a full list of teams with players and subs for selected scrim.\nPlus a total team, player and sub count.\n\n**Usage:** \*optional\*\n/team_list",
    "last_updated": "Last Updated: v1.2.0 | xx/07/2024",
    },
"register_trio": {
    "warning": ":warning: *Renamed and Reworked in v1.1.0 (was `/register`)*",
    "small_text": "Register a trio team for Scrims",
    "description": "Register a trio team for Scrims.\nInclude 3 players, upto 2 subs and an optional team logo.\nA dropdown will appear with all scheduled scrims to join\n\n**Usage:** \*optional\*\n`/register_trio team_name: player1: player2: player3: *sub1*: *sub2*: *logo*:`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"register_duo": {
    "warning": ":bulb: *New in v1.1.0*",
    "small_text": "Register a duo team for Scrims",
    "description": "Register a duo team for Scrims.\nInclude 2 players, upto 2 subs and an optional team logo.\nA dropdown will appear with all scheduled scrims to join\n\n**Usage:** \*optional\*\n`/register_duo team_name: player1: player2: *sub1*: *sub2*: *logo*:`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"register_solo": {
    "warning": ":bulb: *New in v1.1.0*",
    "small_text": "Register a solo team for Scrims",
    "description": "Register a solo team for Scrims.\nInclude 1 player and an optional team logo.\nA dropdown will appear with all scheduled scrims to join\n\n**Usage:** \*optional\*\n`/register_solo player_name: *logo*:`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"schedule": {
    "warning": ":warning: *Majorly Updated in v1.1.0*",
    "small_text": "Schedule Scrims",
    "description": "**Admin Only**\nSchedule Scrims.\nOpens a series of menus to customise and schedule scrims\nPlus creating a Discord event for Scrims.\n\n**Usage:** \*optional\*\n`/schedule`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"help": {
    "warning": ":warning: *Majorly Updated in v1.1.0*",
    "small_text": "Opens a help",
    "description": "Opens a help menu, use the dropdown to get help on that command.\nFind more information on each command and more.\n\n**Usage:** \*optional\*\n`/help`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"configure": {
    "warning": ":warning: *Reworked in v1.1.0*",
    "small_text": "Configure Scrimotron for your server",
    "description": "**Admin Only**\nConfigure Scrimotron for your server.\nOpens a series of menus.\nMost things in scrimotron can be altered to your server's needs\n\n**Usage:** \*optional\*\n`/configure`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"score": {
    "warning": None,
    "small_text": "Calculate Scores Automatically",
    "description": "**Admin Only**\nCalculate Scores Automatically.\nGo to https://apexlegendsstatus.com/tournament/ and create a tournament to get scores.\nOutputs scores in a leaderboard and attaches spreadsheet!\n\n**Usage:** \*optional\*\n`/score tournament_id`",
    "last_updated": "Last Updated: v1.0.0 | 23/04/2024",
    },
"feedback": {
    "warning": ":bulb: *New in v1.1.0*",
    "small_text": "Submit Feedback/Suggestions/Bug Reports to Catotron",
    "description": "Submit Feedback/Suggestions/Bug Reports to Catotron.\nOpens a form to enter feedback which is directly sent to Catotron.\n\n**Usage:** \*optional\*\n`/feedback`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
"scrims": {
    "warning": ":bulb: *New in v1.1.0*",
    "small_text": "View and edit all currently scheduled scrims",
    "description": "**Admin Only**\nView and edit all currently scheduled scrims.\nView all scrims with basic information\n**OR**\nView one scrim with all information and option to make edits.\n\n**Usage:** \*optional\*\n`/scrims`",
    "last_updated": "Last Updated: v1.1.0 | 26/06/2024",
    },
}

class dropdown_menu(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.add_item(dropdown_help_menu(interaction))

class dropdown_help_menu(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction):
        self.interaction = interaction
        if self.interaction.user.guild_permissions.administrator == True: super().__init__(placeholder="Select a command", min_values=1, max_values=1, options=[nextcord.SelectOption(label=i, value=i) for i in admin_command_list])
        else: super().__init__(placeholder="Select a command", min_values=1, max_values=1, options=[nextcord.SelectOption(label='/'+i, value=i) for i in public_command_list])

    async def callback(self, interaction: nextcord.Interaction):
        try:
            if help_descriptions[interaction.data['values'][0]]["warning"] == None: embed = nextcord.Embed(title=f"Help Menu | /{interaction.data['values'][0]}", description=f"\n{help_descriptions[interaction.data['values'][0]]['description']}", color=White)
            else: embed = nextcord.Embed(title=f"Help Menu | /{interaction.data['values'][0]}", description=f"\n{help_descriptions[interaction.data['values'][0]]['warning']}\n{help_descriptions[interaction.data['values'][0]]['description']}", color=White)

            embed.set_footer(text=f"/{interaction.data['values'][0]} {help_descriptions[interaction.data['values'][0]]['last_updated']}")
            await interaction.response.edit_message(embed=embed, view=dropdown_menu(self.interaction))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class Command_help_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="help", description="Open a help menu for information on all commands")
    async def help(self, interaction: nextcord.Interaction):
        global command
        command = {"name": interaction.application_command.name, "userID": interaction.user.id, "guildID": interaction.guild.id}
        formatOutput(output=f"/{command['name']} Used by {command['userID']} | @{interaction.user.name}", status="Normal", guildID=command["guildID"])

        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        embed = nextcord.Embed(title="Help Menu", description="Find the command in the dropdown to get help on that command.", color=White)
        await interaction.edit_original_message(embed=embed, view=dropdown_menu(interaction))

def setup(bot):
    bot.add_cog(Command_help_Cog(bot))