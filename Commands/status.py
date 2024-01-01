import nextcord
import traceback
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse
from Config import db_bot_data, db_team_data

class Command_status_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="status", description="Show Tournament Status", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def status(self, interaction: nextcord.Interaction):
        command = 'status'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer(ephemeral=True)
        try:
            pois_selected = teams_checked_in = 0
            status_data = db_bot_data.find_one({"setup": {"$exists": True}})
            team_data = list(db_team_data.find())

            embed = nextcord.Embed(title="United Status", description="", color=0x000)

            # setup status
            if status_data != None:
                if status_data["setup"] == "yes": embed.add_field(name="Setup", value="**Complete**", inline=True)
                else: embed.add_field(name="Setup", value="**Awaiting Automation**", inline=True)
            else: embed.add_field(name="Setup", value="*United has not been scheduled yet*", inline=True)

            # poi status
            if status_data != None:
                if status_data["poi"] == "yes": 
                    for i in team_data:
                        if i["pois"]["map1"] != "None" and i["pois"]["map2"] != "None":
                            pois_selected += 1
                    embed.add_field(name="POI Selections", value=f"**{pois_selected}/{len(team_data)} Teams Selected**", inline=True)
                else: embed.add_field(name="POI Selections", value="**Awaiting Automation**", inline=True)
            else: embed.add_field(name="POI Selections", value="*United has not been scheduled yet*", inline=True)

            # checkin status
            if status_data != None:
                if status_data["checkin"] == "yes":
                    for i in team_data:
                        if i["setup"]["check_in"] != "no":
                            teams_checked_in += 1
                    embed.add_field(name="Check ins", value=f"**{teams_checked_in}/{len(team_data)} Teams Checked In**", inline=True)
                else: embed.add_field(name="Check ins", value="**Awaiting Automation**", inline=True)
            else: embed.add_field(name="Check ins", value="*United has not been scheduled yet*", inline=True)

            # Time until event (hours)
            events = []
            async for event in interaction.guild.fetch_scheduled_events():
                events.append(event)

            if not events:
                embed.add_field(name="Time Until Event", value="**/schedule**", inline=True)
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
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_status_Cog(bot))