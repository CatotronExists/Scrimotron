import nextcord
import openpyxl
import datetime
import shutil
from nextcord.ext import commands
from Main import formatOutput, errorResponse
import requests
from Keys import API_TOKEN
from BotData.colors import *
import traceback

class Command_score_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="score", description="Calculate Scores Automatically. **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def score(self, interaction: nextcord.Interaction,
        id = nextcord.SlashOption(name="tournament_id", description="Tournament Code, Found in the link: apexlegendsstatus.com/tournament/results/**500**", required=True)):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        embed = nextcord.Embed(title="Calculating Scores", description="Please wait, this may take some time...", color=White)
        await interaction.edit_original_message(embed=embed)

        if id.isnumeric() == True:
            id = int(id)

            try:
                url = f"https://apexlegendsstatus.com/tournament/ingram/?qt=getScores&tournamentId={id}"

                headers = {
                    'Authorization': API_TOKEN,
                }

                api_data = requests.get(url, headers=headers)
                api_data = api_data.json()

                placement = 0
                leaderboard_data = ["Scrim Scoreboard", "**Placement** | **Team Name** | **Points**"]
                highest_damage = ["", 0, ""] # pname, damage, pteam
                highest_kills = ["", 0, ""] # pname, kills, pteam

                for team in api_data["teamData"]:
                    placement += 1
                    leaderboard_data.append(f"#{placement}  | {team['teamName']} | {team['points']}")
                    for player in team["playersData"]:
                        if player["damageDealt"] > highest_damage[1]:
                            highest_damage = [player["playerName"], player["damageDealt"], team["teamName"]]

                        if player["kills"] > highest_kills[1]:
                            highest_kills = [player["playerName"], player["kills"], team["teamName"]]
            
                leaderboard_data.append("**Other Data**")
                leaderboard_data.append(f"Highest Damage: {highest_damage[1]} - {highest_damage[0]} ({highest_damage[2]})")
                leaderboard_data.append(f"Highest Kills: {highest_kills[1]} - {highest_kills[0]} ({highest_kills[2]})")

                data = "\n".join(leaderboard_data)
                embed = nextcord.Embed(title="Scores Calculated", description=data, color=White)


                # Spreadsheet Creation
                tournament_name = api_data["ALSData"]["name"]
                if "/" in tournament_name: tournament_name = tournament_name.replace("/", "-")
                spreadsheet_name = f"Spreadsheet-{tournament_name}.xlsx"
                shutil.copy("scrimotron/Spreadsheets/Spreadsheet Template.xlsx", f"scrimotron/Spreadsheets/{spreadsheet_name}")
                excel_file = openpyxl.load_workbook(f"scrimotron/Spreadsheets/{spreadsheet_name}")
                sheet = excel_file.active

                row = 4
                number_of_teams = 0
                for team in api_data["teamData"]:
                    sheet[f"A{row}"] = team["teamName"]
                    rankings = team["ranking"]
                    sheet[f"E{row}"] = team["kills"]

                    try: # Covers for any out of index errors (if 6 games weren't played)
                        if rankings[0] <= 0: sheet[f"G{row}"] = 0 
                        else: sheet[f"G{row}"] = rankings[0]

                        if rankings[1] <= 0: sheet[f"J{row}"] = 0
                        else: sheet[f"J{row}"] = rankings[1]

                        if rankings[2] <= 0: sheet[f"M{row}"] = 0
                        else: sheet[f"M{row}"] = rankings[2]

                        if rankings[3] <= 0: sheet[f"P{row}"] = 0
                        else: sheet[f"P{row}"] = rankings[3]

                        if rankings[4] <= 0: sheet[f"S{row}"] = 0
                        else: sheet[f"S{row}"] = rankings[4]

                        if rankings[5] <= 0: sheet[f"V{row}"] = 0
                        else: sheet[f"V{row}"] = rankings[5]
                    except: pass

                    row += 1
                    number_of_teams += 1

                if number_of_teams < 30: # Clears any placeholder rows if there are less than 30 teams
                    while row < 34:
                        # Clear Totals
                        sheet[f"A{row}"] = ""
                        sheet[f"B{row}"] = ""
                        sheet[f"C{row}"] = ""
                        sheet[f"D{row}"] = ""
                        sheet[f"E{row}"] = ""

                        # Clear Unused Placement Formulars
                        sheet[f"H{row}"] = ""
                        sheet[f"K{row}"] = ""
                        sheet[f"N{row}"] = ""
                        sheet[f"Q{row}"] = ""
                        sheet[f"T{row}"] = ""
                        sheet[f"W{row}"] = ""

                        row += 1

                excel_file.save(f"scrimotron/Spreadsheets/{spreadsheet_name}")
                excel_file.close()

                with open(f'scrimotron/Spreadsheets/{spreadsheet_name}', 'rb') as fp:
                    await interaction.edit_original_message(embed=embed, file=nextcord.File(fp, spreadsheet_name))
                
                fp.close() # not actually closing the file, restart to be able to delete it
            
            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)

        else: 
            embed = nextcord.Embed(title="Error", description="Tournament IDs must be numeric (e.g 500)", color=Red)
            await interaction.edit_original_message(embed=embed)

def setup(bot):
    bot.add_cog(Command_score_Cog(bot))

# bot hosting requires scrimotron/(path)