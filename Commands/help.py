import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, public_command_list, admin_command_list

help_descriptions = {
"team_list": "\nShows a full list of teams, Captains, Players and Subs. Also a total team, player and sub count.\n\n**Usage:** *optional*\n/team_list\n**Example:**\n/team_list",
"register": "\nRegister your team for United.\n\n**Usage:** *optional*\n/register team_name: captain: player2: player3: *sub1*: *sub2*: *logo*:\n**Example:**\n/register BestTeamEver @DrunkBoater @TTV-Wraith @Hotdropper @IamASUBmarine",
"unregister": "\nUnregister your team from United.\n\n**Usage:** *optional*\n/unregister team_name:\n**Example:**\n/unregister BestTeamEver",
"start": "**Admin Only**\nStart UnitedOCE, Creates Roles and VCs for teams.\n**Usage:** *optional*\n/start\n**Example:**\n/start",
"end": "**Admin Only**\nEnd UnitedOCE, Deletes Roles and VCs for teams.\n**Usage:** *optional*\n/end\n**Example:**\n/end",
"check_in": "**Admin Only**\nOpen check ins for UnitedOCE.\n**Usage:** *optional*\n/check_in\n**Example:**\n/check_in",
"schedule": "**Admin Only**\nSchedule UnitedOCE. Creates a Discord event for United\n**Usage:** *optional*\n/schedule date: (in dd/mm/yyyy) time: x:yyam/pm timezone:\n**Example:**\n/schedule 22/10/2023 7pm AEDT",
"open_poi": "**Admin Only**\nOpen POI Selections for UnitedOCE.\n**Usage:** *optional*\n/open_poi map1: map2:\n**Example:**\n/open_poi Worlds Edge Broken Moon",
"select_poi": "\nSelect a POI for your team.\n\n**Usage:** *optional*\n/select_poi\n**Example:**\n/select_poi",
"help": "\nOpens a help menu, click on any button to get help on that command, Find Example usage and more.\n**Usage:** *optional*\n/help\n**Example:**\n/help",
"unregister_all": "**Admin Only**\nUnregister all teams from UnitedOCE.\n**Usage:** *optional*\n/unregister_all\n**Example:**\n/unregister_all"
}

class Command_name_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class help_buttons(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction):
            super().__init__()
            self.interaction = interaction
        
            if self.interaction.user.guild_permissions.administrator == True: command_list = admin_command_list
            else: command_list = public_command_list
            for i in command_list:
                button = nextcord.ui.Button(label=f"/{i}", style=nextcord.ButtonStyle.blurple)
                button.callback = self.create_callback(i, help_descriptions)
                self.add_item(button)
        
        def create_callback(self, label, help_descriptions):
            async def callback(interaction: nextcord.Interaction):
                try:
                    embed = nextcord.Embed(title=f"Help Menu | /{label}", description=help_descriptions[label], color=0x000)
                    embed.set_footer(text="Help Menu")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                except Exception as e:
                    await errorResponse(error=e, command="help", interaction=interaction)
            return callback

    @nextcord.slash_command(guild_ids=[guildID], name="help", description="Open the help menu")
    async def help(self, interaction: nextcord.Interaction):
        command = 'help'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        try: await interaction.response.defer(ephemeral=True)
        except: pass
        
        embed = nextcord.Embed(title="Help Menu", description="Click a button to get help on that command.", color=0x000)
        embed.set_footer(text="Press one of the buttons below")
        await interaction.edit_original_message(embed=embed, view=self.help_buttons(interaction))

def setup(bot):
    bot.add_cog(Command_name_Cog(bot))