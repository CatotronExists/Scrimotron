import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getTeams
from BotData.colors import *

class Command_team_list_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="team_list", description="Shows a list of all the teams that have been registered")
    async def team_list(self, interaction: nextcord.Interaction):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        message = []
        try:
            data = getTeams(guildID)
            teams = players = subs = 0
            for i in data:
                if i["teamSub1"] == "N/A" and i["teamSub2"] == "N/A":
                    message.append(f"**{i['teamName']}** - **C:** {self.bot.get_user(int(i['teamCaptain'])).mention} - **P:** {self.bot.get_user(int(i['teamPlayer2'])).mention} & {self.bot.get_user(int(i['teamPlayer3'])).mention}")
                elif i["teamSub2"] == "N/A":
                    subs += 1
                    message.append(f"**{i['teamName']}** - **C:** {self.bot.get_user(int(i['teamCaptain'])).mention} - **P:** {self.bot.get_user(int(i['teamPlayer2'])).mention} & {self.bot.get_user(int(i['teamPlayer3'])).mention} - **S:** {self.bot.get_user(int(i['teamSub1'])).mention}")
                else:
                    subs += 2
                    message.append(f"**{i['teamName']}** - **C:** {self.bot.get_user(int(i['teamCaptain'])).mention} - **P:** {self.bot.get_user(int(i['teamPlayer2'])).mention} & {self.bot.get_user(int(i['teamPlayer3'])).mention} - **S:** {self.bot.get_user(int(i['teamSub1'])).mention} & {self.bot.get_user(int(i['teamSub2'])).mention}")
                players += 3
                teams += 1

            embed = nextcord.Embed(title="Registered Teams", description='\n'.join(message), color=White)
            embed.set_footer(text=f"Total Teams: {teams} | Total Players: {players} | Total Subs: {subs}")
            await interaction.edit_original_message(embed=embed)
            formatOutput(output=f"   /{command} was successful!", status="Good", guildID=guildID)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_team_list_Cog(bot))