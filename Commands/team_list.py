import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse
from Config import db_team_data

class Command_team_list_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="team_list", description="List all registered teams")
    async def team_list(self, interaction: nextcord.Interaction):
        command = 'team_list'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer()

        message = []
        try:
            data = list(db_team_data.find())
            teams = players = subs = 0
            for i in data:
                if i["sub1"] == "N/A" and i["sub2"] == "N/A":
                    message.append(f"**{i['team_name']}** - **C:** {self.bot.get_user(int(i['captain'])).mention} - **P:** {self.bot.get_user(int(i['player2'])).mention} & {self.bot.get_user(int(i['player3'])).mention}")
                elif i["sub2"] == "N/A":
                    subs += 1
                    message.append(f"**{i['team_name']}** - **C:** {self.bot.get_user(int(i['captain'])).mention} - **P:** {self.bot.get_user(int(i['player2'])).mention} & {self.bot.get_user(int(i['player3'])).mention} - **S:** {self.bot.get_user(int(i['sub1'])).mention}")
                else:
                    subs += 2
                    message.append(f"**{i['team_name']}** - **C:** {self.bot.get_user(int(i['captain'])).mention} - **P:** {self.bot.get_user(int(i['player2'])).mention} & {self.bot.get_user(int(i['player3'])).mention} - **S:** {self.bot.get_user(int(i['sub1'])).mention} & {self.bot.get_user(int(i['sub2'])).mention}")
                players += 3
                teams += 1

            embed = nextcord.Embed(title="Registered Teams", description='\n'.join(message), color=0x000)
            embed.set_footer(text=f"Total Teams: {teams} | Total Players: {players} | Total Subs: {subs}")
            await interaction.edit_original_message(embed=embed)
            formatOutput(output=f"   /{command} was successful!", status="Good")

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_team_list_Cog(bot))