import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, public_command_list, admin_command_list
from BotData.colors import *

help_descriptions = {
"team_list": "\nShows a full list of teams, Captains, Players and Subs. Also a total team, player and sub count.\n\n**Usage:** *optional*\n/team_list\n**Example:**\n`/team_list`",
"register": "\nRegister your team for Scrims.\n\n**Usage:** *optional*\n`/register team_name: captain: player2: player3: *sub1*: *sub2*: *logo*:`\n**Example:**\n`/register` `BestTeamEver` `@DrunkBoater` `@TTV-Wraith` `@Hotdropper` `@IamA_SUBmarine`",
"end": "**Admin Only**\nEnd Scrims, Deletes Roles and VCs for teams.\nAlso starts tallying scores\n**Usage:** *optional*\n`/end`\n**Example:**\n`/end`",
"schedule": "**Admin Only**\nSchedule Scrims. Creates a Discord event for Scrims. Starts Automated process leading up to the start of scrims.\n**Usage:** *optional*\n`/schedule name: time: (in epoch) map1: map2: selection_mode:`\n**Example:**\n`/schedule` `3133648800` `Worlds Edge` `Storm Point` `Simple`",
"select_poi": "\nSelect a POI for your team.\n\n**Usage:** *optional*\n`/select_poi]`\n**Example:**\n`/select_poi`",
"help": "\nOpens a help menu, use the dropdown to get help on that command, Find Example usage and more.\n**Usage:** *optional*\n`/help`\n**Example:**\n`/help`",
"unregister_all": "**Admin Only**\nUnregister all teams from Scrims.\n**Usage:** *optional*\n`/unregister_all`\n**Example:**\n`/unregister_all`",
"status": "**Admin Only**\nShow the status of Scrims. Current amount of teams checked in and POIs selected.\n**Usage:** *optional*\n`/status`\n**Example:**\n`/status`",
"configure": "**Admin Only**\nConfigure the bot for your server. Opens a series of menus\n**Usage:** *optional*\n`/configure`\n**Example:**\n`/configure`",
"score": "**Admin Only**\nCalculate Scores Automatically. Go to https://apexlegendsstatus.com/tournament/ and create a tournament to get scores\n**Usage:** *optional*\n`/score tournament_id`\n**Example:**\n`/score` `500`"
}
#"command_name": "((**Admin Only**))\nBrief Discription.\nQuick Quide.\n**Usage:** *optional*\n`/command_name example_option:`\n**Example:**\n`/command_name` `example`"

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
            embed = nextcord.Embed(title=f"Help Menu | /{interaction.data['values'][0]}", description=help_descriptions[interaction.data['values'][0]], color=0x000)
            embed.set_footer(text="Help Menu")
            await interaction.response.send_message(embed=embed, ephemeral=True, view=dropdown_menu(self.interaction))
        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

class Command_help_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="help", description="Open a help menu for information on all commands. Plus examples of usage")
    async def help(self, interaction: nextcord.Interaction):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass
        
        embed = nextcord.Embed(title="Help Menu", description="Find the command in the dropdown to get help on that command.", color=White)
        embed.set_footer(text="Use the dropdown below")
        await interaction.edit_original_message(embed=embed, view=dropdown_menu(interaction))

def setup(bot):
    bot.add_cog(Command_help_Cog(bot))