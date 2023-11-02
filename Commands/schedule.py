import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse
import re

class Command_schedule_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="schedule", description="Schedule United", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def schedule(self, interaction: nextcord.Interaction, date: str, time: str, timezone: str):
        command = 'schedule'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.response.defer(ephemeral=True)
        error = False

        try: # Get time and date
            date = date.split("/")
            day = date[0]
            month = date[1]
            year = date[2]
            hour = re.search(r"\d+", time).group()
            am_pm = re.search(r"[AaPp][Mm]", time).group()
            am_pm = am_pm.lower() # converts to lowercase
            try: minute = re.search(r":\d+", time).group()[1:]
            except: minute = "00" # if no minute is given, set to 00
            dateandtime = datetime.datetime.strptime(f"{day}/{month}/{year} {hour}:{minute} {am_pm}", "%d/%m/%Y %I:%M %p")

        except Exception as e: 
            await errorResponse(error=e, command=command, interaction=interaction)

        try: # Create Event
            if error == False:
                await interaction.send(f"Scheduling United for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone}", ephemeral=True)
                image = "https://cdn.discordapp.com/attachments/1166164223672471622/1167256572897009704/twitter_header.png"
                dateandtime = dateandtime + datetime.timedelta(hours=13) # Temp utc offset fix
                await interaction.guild.create_scheduled_event(
                    name="United OCE Test Round", 
                    description="This is a test round of United OCE, [A description about united, maybe a link to recent announcement?. anyway, this is a test round]", 
                    entity_type=nextcord.ScheduledEventEntityType.external, 
                    metadata=nextcord.EntityMetadata(location="APAC-South"),
                    start_time=dateandtime,
                    end_time=dateandtime + datetime.timedelta(hours=2),
                    privacy_level=nextcord.ScheduledEventPrivacyLevel.guild_only, 
                    reason="Weekly UnitedOCE Event" 
                    #image=image #Breaks,
                    )
                await interaction.edit_original_message(content=f"United has been scheduled for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone}")
                formatOutput(output=f"   United has been scheduled for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone}", status="Good")
                formatOutput(output=f"   /{command} was successful!", status="Good")
                
        except Exception as e: 
            await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_schedule_Cog(bot))