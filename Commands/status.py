import nextcord
import traceback
import datetime
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getTeams, getScrimSetup, getScrimInfo, getConfigData
from BotData.colors import *

class Command_status_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="status", description="Shows the status of scrims. **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def status(self, interaction: nextcord.Interaction):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass        
        
        try:
            pois_selected = teams_checked_in = 0
            setup_data = getScrimSetup(guildID)
            team_data = getTeams(guildID)
            scrim_info = getScrimInfo(guildID)
            config_data = getConfigData(guildID)
            embed = nextcord.Embed(title=scrim_info["ScrimName"], description="", color=White)

            # checkin status
            if config_data["toggleCheckin"] == True:
                for team in team_data:
                        if team["teamStatus"]["checkin"] == True:
                            teams_checked_in += 1
                embed.add_field(name="Check ins", value=f"**{teams_checked_in}/{len(team_data)} Teams Checked In**", inline=True)
            else: embed.add_field(name="Check ins", value="**Disabled**", inline=True)

            # poi status
            if config_data["togglePoi"] == True:
                for team in team_data:
                    if team["teamStatus"]["poiSelection"] == True:
                        pois_selected += 1
                embed.add_field(name="POI Selections", value=f"**{pois_selected}/{len(team_data)} Teams Selected**", inline=True)
            else: embed.add_field(name="Poi Selections", value="**Disabled**", inline=True)

            # setup status
            if config_data["toggleSetup"] == True:
                if setup_data["complete"]["setupComplete"] == True: embed.add_field(name="Setup", value="**Complete**", inline=True)
                else: embed.add_field(name="Setup", value="**Awaiting Automation**", inline=True)
            else: embed.add_field(name="Setup", value="**Disabled**", inline=True)

            # Time until event (hours)
            events = []
            async for event in interaction.guild.fetch_scheduled_events():
                events.append(event)

            if not events:
                embed.add_field(name="Time Until Event", value="**No Scheduled Scrims**", inline=True)
            else:
                for event in events:
                    time_until_start = event.start_time - datetime.datetime.now(datetime.timezone.utc)
                if time_until_start.total_seconds() < 0:
                    embed.add_field(name="Time Until Event", value="**Event Started**", inline=True)
                elif time_until_start.total_seconds() < 3600:
                    embed.add_field(name="Time Until Event", value=f"**{round(time_until_start.total_seconds() / 60)} Minutes**", inline=True)
                else:
                    embed.add_field(name="Time Until Event", value=f"**{round(time_until_start.total_seconds() / 3600)} Hours**", inline=True)

            await interaction.edit_original_message(embed=embed)
    
        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_status_Cog(bot))