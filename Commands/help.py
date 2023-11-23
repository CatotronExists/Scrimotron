import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, public_command_list, admin_command_list

help_descriptions = {
"team_list": "\nShows a full list of teams, Captains, Players and Subs. Also a total team, player and sub count.\n\n**Usage:** *optional*\n/team_list\n**Example:**\n/team_list",
"register": "\nRegister your team for United.\n\n**Usage:** *optional*\n/register team_name: captain: player2: player3: *sub1*: *sub2*: *logo*:\n**Example:**\n/register BestTeamEver @DrunkBoater @TTV-Wraith @Hotdropper @IamASUBmarine",
"unregister": "\nUnregister your team from United.\n\n**Usage:** *optional*\n/unregister team_name:\n**Example:**\n/unregister BestTeamEver",
"end": "**Admin Only**\nEnd UnitedOCE, Deletes Roles and VCs for teams.\n**Usage:** *optional*\n/end\n**Example:**\n/end",
"schedule": "**Admin Only**\nSchedule UnitedOCE. Creates a Discord event for United. Starts Automated process leading up to United.\n**Usage:** *optional*\n/schedule date: (in dd/mm/yyyy) time: H*:MM*am/pm timezone: map1: map2:\n**Example:**\n/schedule 22/10/2023 7pm AEDT Worlds Edge Storm Point",
"select_poi": "\nSelect a POI for your team.\n\n**Usage:** *optional*\n/select_poi\n**Example:**\n/select_poi",
"help": "\nOpens a help menu, use the dropdown to get help on that command, Find Example usage and more.\n**Usage:** *optional*\n/help\n**Example:**\n/help",
"unregister_all": "**Admin Only**\nUnregister all teams from UnitedOCE.\n**Usage:** *optional*\n/unregister_all\n**Example:**\n/unregister_all",
"status": "**Admin Only**\nShow the status of UnitedOCE. Current amount of teams checked in and POIs selected.\n**Usage:** *optional*\n/status\n**Example:**\n/status",
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
            embed = nextcord.Embed(title=f"Help Menu | /{interaction.data['values'][0]}", description=help_descriptions[interaction.data['values'][0]], color=0x000)
            embed.set_footer(text="Help Menu")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command="help", interaction=interaction)

class Command_help_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="help", description="Open the help menu")
    async def help(self, interaction: nextcord.Interaction):
        command = 'help'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        try: await interaction.response.defer(ephemeral=True)
        except: pass
        
        embed = nextcord.Embed(title="Help Menu", description="Find the command in the dropdown to get help on that command.", color=0x000)
        embed.set_footer(text="Use the dropdown below")
        await interaction.edit_original_message(embed=embed, view=dropdown_menu(interaction))

def setup(bot):
    bot.add_cog(Command_help_Cog(bot))