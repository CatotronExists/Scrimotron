import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getChannels, getMessages, splitMessage
from Keys import DB
from BotData.colors import *

class Command_schedule_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="schedule", description="Schedule Scrims. Starts Automation Process for Checkins, POI selections and team VCs. **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def schedule(self, interaction: nextcord.Interaction,
        name = nextcord.SlashOption(name="name", description="Scrim Name", required=True),
        epoch = nextcord.SlashOption(name="time", description="Scrim Starting Time (in epoch), Use https://www.epochconverter.com/", required=True),
        map1 = nextcord.SlashOption(name="map_1", description="Choose map 1", required=True, choices={"World's Edge": "Worlds Edge", "Olympus": "Olympus", "King's Canyon": "Kings Canyon", "Storm Point": "Storm Point", "Broken Moon": "Broken Moon"}),
        map2 = nextcord.SlashOption(name="map_2", description="Choose map 2", required=True, choices={"World's Edge": "Worlds Edge", "Olympus": "Olympus", "King's Canyon": "Kings Canyon", "Storm Point": "Storm Point", "Broken Moon": "Broken Moon"}),
        selection_mode = nextcord.SlashOption(name="selection_mode", description="Choose selection mode", required=True, choices={"Simple": "Simple"})#, "Advanced": "Advanced"}))
        ):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        dateandtime = datetime.datetime.fromtimestamp(int(epoch))
        discord_time = dateandtime - datetime.timedelta(hours=10) # discord schedules events 10 hours ahead? UTC thing? help??
        formatted_time = nextcord.utils.format_dt(dateandtime, "f")

        try: # Create Event
                #image = ""
                await interaction.guild.create_scheduled_event(
                    name=name, 
                    description=f"Maps: {map1} & {map2} | Selection Mode: {selection_mode}", 
                    entity_type=nextcord.ScheduledEventEntityType.external, 
                    metadata=nextcord.EntityMetadata(location=interaction.guild.name),
                    start_time=discord_time,
                    end_time=discord_time + datetime.timedelta(hours=2),
                    privacy_level=nextcord.ScheduledEventPrivacyLevel.guild_only, 
                    reason="Scrim Scheduled by Scrimotron"
                    #image=image #Breaks due to limitations in discord API. Images have to be local files not URLs, Potential fix/workaround later?
                    )
                DB[str(guildID)]["ScrimData"].update_one({"scrimSetup": {"$exists": True}}, {"$set": {"scrimSetup.complete.poiComplete": False, "scrimSetup.complete.checkinComplete": False, "scrimSetup.complete.setupComplete": False, "scrimSetup.maps.map1": map1, "scrimSetup.maps.map2": map2, "scrimSetup.poiSelectionMode": selection_mode}})
                DB[str(guildID)]["ScrimData"].update_one({"scrimInfo": {"$exists": True}}, {"$set": {"scrimInfo.scrimName": name ,"scrimInfo.scrimEpoch": epoch}})
                await interaction.send(content=f"{name} has been scheduled for {formatted_time}\n`Maps: {map1} & {map2}`\n`Selection Mode: {selection_mode}`", ephemeral=True)
                
                channels = getChannels(guildID)
                if channels["scrimRegistrationChannel"] != None:
                    channel = interaction.guild.get_channel(channels["scrimRegistrationChannel"])

                    messages = getMessages(interaction.guild.id)
                    message = splitMessage(messages["scrimRegistration"], interaction.guild.id)
                    message_split = message.split("\n")
                    title = message_split[0]
                    description = '\n'.join(message_split[1:])

                    embed = nextcord.Embed(title=title, description=description, color=White)
                    await channel.send(embed=embed)
                
                else:
                    embed = nextcord.Embed(title="Scrim Registration", description="Scrim Registration Channel not set. Please set it up using `/setup`", color=Red)
                    channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)
                
                channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                embed = nextcord.Embed(title=f"{name} has been Scheduled", description=f"{name} was scheduled for {formatted_time}\n `Maps: {map1} & {map2}`\n`Selection Mode: {selection_mode}`", color=Green)
                embed.set_footer(text=f"Scheduled at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC by @{interaction.user.name}")
                await channel.send(embed=embed)

                formatOutput(output=f"   {name} has been scheduled | Maps: {map1} & {map2} | Mode: {selection_mode}", status="Good", guildID=guildID)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_schedule_Cog(bot))