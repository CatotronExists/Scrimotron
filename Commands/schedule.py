import nextcord
import datetime
import traceback
import re
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_bot_event, checkin, poi_selection
from Config import db_bot_data

class Command_schedule_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="schedule", description="Schedule United", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def schedule(self, interaction: nextcord.Interaction,
        name = nextcord.SlashOption(name="name", description="Name of the event", required=True),
        date = nextcord.SlashOption(name="date", description="Date of the event (DD/MM/YYYY)", required=True),
        time = nextcord.SlashOption(name="time", description="Time of the event (HH:MM AM/PM)", required=True),
        timezone = nextcord.SlashOption(name="timezone", description="Timezone of the event (eg. AEDT/AEST)", required=True),
        map1 = nextcord.SlashOption(name="map_1", description="Choose map 1", required=True, choices={"World's Edge": "Worlds Edge", "Olympus": "Olympus", "King's Canyon": "Kings Canyon", "Storm Point": "Storm Point", "Broken Moon": "Broken Moon"}),
        map2 = nextcord.SlashOption(name="map_2", description="Choose map 2", required=True, choices={"World's Edge": "Worlds Edge", "Olympus": "Olympus", "King's Canyon": "Kings Canyon", "Storm Point": "Storm Point", "Broken Moon": "Broken Moon"}),
        selection_mode = nextcord.SlashOption(name="selection_mode", description="Choose selection mode", required=True, choices={"Simple": "Simple", "Advanced": "Advanced"})
        ):
        command = 'schedule'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer(ephemeral=True)
        error = False

        try:
            try: db_bot_data.delete_one({"maps": {"$exists": True}}) # remove old maps
            except: pass
            try: db_bot_data.update_one({"maps": {"map1": map1, "map2": map2, "selection_mode": selection_mode}})
            except: db_bot_data.insert_one({"maps": {"map1": map1, "map2": map2, "selection_mode": selection_mode}})

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
            error = True

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
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
            error = True

        try: # Create Event
            if error == False:
                await interaction.send(f"Scheduling United for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone}", ephemeral=True)
                #image = "https://cdn.discordapp.com/attachments/1166164223672471622/1167256572897009704/twitter_header.png"
                dateandtime = dateandtime + datetime.timedelta(hours=13) # Temp utc offset fix
                dateandtime = dateandtime - datetime.timedelta(days=1) # Temp one day off fix
                await interaction.guild.create_scheduled_event(
                    name=name, 
                    description=f"This is a test round of United OCE, [A description about united, maybe a link to recent announcement?. anyway, this is a test round]\nPOI Selections open {poi_selection} hours before start\nCheck ins open {checkin} hour before start\nMaps: {map1} & {map2} | Selection Mode: {selection_mode}", 
                    entity_type=nextcord.ScheduledEventEntityType.external, 
                    metadata=nextcord.EntityMetadata(location="APAC-South"),
                    start_time=dateandtime,
                    end_time=dateandtime + datetime.timedelta(hours=2),
                    privacy_level=nextcord.ScheduledEventPrivacyLevel.guild_only, 
                    reason="Weekly UnitedOCE Event"
                    #image=image #Breaks due to limitations in discord API. Images have to be local files not URLs,
                    )
                db_bot_data.update_one({"setup": {"$exists": True}}, {"$set": {"setup": 'no', "checkin": 'no', "poi": 'no'}})
                await interaction.edit_original_message(content=f"United has been scheduled for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone}\n`Maps: {map1} & {map2}`\n`Selection Mode: {selection_mode}`")
                
                channel = interaction.guild.get_channel(channel_bot_event)
                embed = nextcord.Embed(title="UnitedOCE has been Scheduled", description=f"The next round of UnitedOCE was scheduled for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone}\n `Maps: {map1} & {map2}`\n`Selection Mode: {selection_mode}`", color=0x008000)
                embed.set_footer(text=f"Scheduled at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC by @{interaction.user.name}")
                await channel.send(embed=embed)

                formatOutput(output=f"   United has been scheduled for {day}/{month}/{year} @ {hour}:{minute} {am_pm} {timezone} | Maps: {map1} & {map2} | Mode: {selection_mode}", status="Good")
                formatOutput(output=f"   /{command} was successful!", status="Good")

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_schedule_Cog(bot))