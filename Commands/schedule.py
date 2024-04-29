import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getChannels, getMessages, splitMessage
from Keys import DB
from BotData.colors import *
from BotData.mapdata import *

class NamingView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        input_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Input Name")
        input_button.callback = self.create_callback("input")
        self.add_item(input_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("cancel")
        self.add_item(cancel_button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            try:
                if custom_id == "input":
                    await interaction.response.send_modal(modal=NamingModal(interaction))

                elif custom_id == "cancel":
                    embed = nextcord.Embed(title="Scrim Scheduling // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class NamingModal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(title="Scrim Name", timeout=None)
        self.interaction = interaction

        self.input = nextcord.ui.TextInput(
            label="Scrim Name",
            style=nextcord.TextInputStyle.short,
            placeholder="Enter Scrim Name", 
            min_length=1, 
            max_length=30)
        
        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            scrim_name = self.input.value
            schedule_data = {"scrim_name": scrim_name}

            embed = nextcord.Embed(title=f"Scrim Scheduling: {schedule_data['scrim_name']} // Time Selection", description="Head to https://www.epochconverter.com/ and get the epoch time.\nScheduling with time and date is no longer supported", color=White)
            await interaction.response.edit_message(embed=embed, view=TimingView(interaction, schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class TimingView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        input_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Input Time")
        input_button.callback = self.create_callback("input")
        self.add_item(input_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("cancel")
        self.add_item(cancel_button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            try:
                if custom_id == "input":
                    await interaction.response.send_modal(modal=TimingModal(interaction, self.schedule_data))

                elif custom_id == "cancel":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class TimingModal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(title="Scrim Time", timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        self.input = nextcord.ui.TextInput(
            label="Scrim Time",
            style=nextcord.TextInputStyle.short,
            placeholder="Enter Scrim Time (in epoch)", 
            min_length=1, 
            max_length=30)
        
        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            scrim_time = self.input.value

            if scrim_time.isnumeric() == True:
                scrim_time = int(scrim_time)
                self.schedule_data["scrim_time"] = scrim_time

                embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Map Selection", description="Select the maps for the scrim", color=White)
                await interaction.response.edit_message(embed=embed, view=MapSelectionView(interaction, self.schedule_data))
            
            else:
                embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Time", description="Please enter a valid epoch time", color=Red)
                await interaction.response.edit_message(embed=embed, view=TimingView(interaction, self.schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
    
class MapSelectionView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data
        self.add_item(MapDropdown(interaction, schedule_data))

class MapDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        self.interaction = interaction
        self.schedule_data = schedule_data

        options = [
            nextcord.SelectOption(label="World's Edge", value="Worlds Edge"),
            nextcord.SelectOption(label="Olympus", value="Olympus"),
            nextcord.SelectOption(label="King's Canyon", value="Kings Canyon"),
            nextcord.SelectOption(label="Storm Point", value="Storm Point"),
            nextcord.SelectOption(label="Broken Moon", value="Broken Moon")
        ]

        super().__init__(placeholder="Select a Map", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            map_name = interaction.data["values"][0]

            if "map_1" not in self.schedule_data: # No map 1 selected yet
                self.schedule_data["map_1"] = map_name
                embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Map Selection", description=f"Map 1 has been selected: **{map_name}**\nAdd a Second Map or Proceed to POI Selection Mode", color=White)
                await interaction.response.edit_message(embed=embed, view=MoreMapView(interaction, self.schedule_data))

            else: # Map 1 already selected -> Set Map 2
                self.schedule_data["map_2"] = map_name
                embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // POI Selection Mode", description=f"Select a POI selection mode from the dropdown below", color=White)
                await interaction.response.edit_message(embed=embed, view=POISelectionView(interaction, self.schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class MoreMapView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        input_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Add Map")
        input_button.callback = self.create_callback("add map")
        self.add_item(input_button)

        proceed_button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="Proceed")
        proceed_button.callback = self.create_callback("proceed")
        self.add_item(proceed_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("cancel")
        self.add_item(cancel_button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            try:
                if custom_id == "add map":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Map Selection", description=f"Map 1: **{self.schedule_data['map_1']}**\nSelect the second map for the scrim", color=White)
                    await interaction.response.edit_message(embed=embed, view=MapSelectionView(interaction, self.schedule_data))

                if custom_id == "proceed":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // POI Selection Mode", description=f"Select a POI selection mode from the dropdown below", color=White)
                    await interaction.response.edit_message(embed=embed, view=POISelectionView(interaction, self.schedule_data))

                elif custom_id == "cancel":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback


class POISelectionView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data
        self.add_item(POIDropdown(interaction, schedule_data))

class POIDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        self.interaction = interaction
        self.schedule_data = schedule_data

        options = [
            nextcord.SelectOption(label="Simple", value="Simple", description="Simply select a whole POI with nothing extra", emoji="📌"),
            ### RETURNING SOON #nextcord.SelectOption(label="Advanced", value="Advanced", description="Select POI halves and nearby smaller POIs", emoji="📊")
            ### SOON #nextcord.SelectOption(label="Random", value="Random", description="POIs are randomly assigned to teams when selections would open", emoji="🎲")
            nextcord.SelectOption(label="No POIs", value="No POIs", description="Disable POI Selection", emoji="❌")
        ]

        super().__init__(placeholder="Select a POI Selection Mode", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            poi_selection_mode = interaction.data["values"][0]
            self.schedule_data["poi_selection_mode"] = poi_selection_mode
            schedule_data = self.schedule_data

            if 'map_2' not in schedule_data: # No map 2
                embed = nextcord.Embed(title=f"Scrim Scheduling: {schedule_data['scrim_name']} // Confirmation", description=f"Confirm Scheduling of: **{schedule_data['scrim_name']}**\n\nTime: <t:{schedule_data['scrim_time']}:f> (**{schedule_data['scrim_time']}**)\nMap: **{schedule_data['map_1']}**\nPOI Selection Mode: **{schedule_data['poi_selection_mode']}**", color=White)
                await interaction.response.edit_message(embed=embed, view=ConfirmationView(interaction, schedule_data))

            else: # Map 2 exists
                embed = nextcord.Embed(title=f"Scrim Scheduling: {schedule_data['scrim_name']} // Confirmation", description=f"Confirm Scheduling of: **{schedule_data['scrim_name']}**\n\nTime: <t:{schedule_data['scrim_time']}:f> (**{schedule_data['scrim_time']}**)\nMaps: **{schedule_data['map_1']}** & **{schedule_data['map_2']}**\nPOI Selection Mode: **{schedule_data['poi_selection_mode']}**", color=White)
                await interaction.response.edit_message(embed=embed, view=ConfirmationView(interaction, schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class ConfirmationView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        confirm_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Confirm")
        confirm_button.callback = self.create_callback("confirm")
        self.add_item(confirm_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("cancel")
        self.add_item(cancel_button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            try:
                if custom_id == "confirm":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Confirmation", description="Scrim is being scheduled, this may take a few moments...", color=White)
                    await interaction.response.edit_message(embed=embed, view=None)

                    ### Save and schedule discord event

                elif custom_id == "cancel":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class Command_schedule_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="schedule", description="Schedule Scrims using a series of menus (Max 5 Scrims at a time). **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def schedule(self, interaction: nextcord.Interaction):

        global command
        command = {"name": interaction.application_command.name, "userID": interaction.user.id, "guildID": interaction.guild.id}
        formatOutput(output=f"/{command['name']} Used by {command['userID']} | @{interaction.user.name}", status="Normal", guildID=command["guildID"])

        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        embed = nextcord.Embed(title="Scrim Scheduling // Name your Scrim", description="What would you like to name your Scrim?", color=White)
        await interaction.edit_original_message(embed=embed, view=NamingView(interaction))

        # dateandtime = datetime.datetime.fromtimestamp(int(epoch))
        # discord_time = dateandtime - datetime.timedelta(hours=10) # discord schedules events 10 hours ahead? UTC thing? help??
        # formatted_time = nextcord.utils.format_dt(dateandtime, "f")

        # try: # Create Event
        #         #image = ""
        #         await interaction.guild.create_scheduled_event(
        #             name=name, 
        #             description=f"Maps: {map1} & {map2} | Selection Mode: {selection_mode}", 
        #             entity_type=nextcord.ScheduledEventEntityType.external, 
        #             metadata=nextcord.EntityMetadata(location=interaction.guild.name),
        #             start_time=discord_time,
        #             end_time=discord_time + datetime.timedelta(hours=2),
        #             privacy_level=nextcord.ScheduledEventPrivacyLevel.guild_only, 
        #             reason="Scrim Scheduled by Scrimotron"
        #             #image=image #Breaks due to limitations in discord API. Images have to be local files not URLs, Potential fix/workaround later?
        #             )
        #         DB[str(guildID)]["ScrimData"].update_one({"scrimSetup": {"$exists": True}}, {"$set": {"scrimSetup.complete.poiComplete": False, "scrimSetup.complete.checkinComplete": False, "scrimSetup.complete.setupComplete": False, "scrimSetup.maps.map1": map1, "scrimSetup.maps.map2": map2, "scrimSetup.poiSelectionMode": selection_mode}})
        #         DB[str(guildID)]["ScrimData"].update_one({"scrimInfo": {"$exists": True}}, {"$set": {"scrimInfo.scrimName": name ,"scrimInfo.scrimEpoch": epoch}})
        #         await interaction.send(content=f"{name} has been scheduled for {formatted_time}\n`Maps: {map1} & {map2}`\n`Selection Mode: {selection_mode}`", ephemeral=True)
                
        #         channels = getChannels(guildID)
        #         if channels["scrimRegistrationChannel"] != None:
        #             channel = interaction.guild.get_channel(channels["scrimRegistrationChannel"])

        #             messages = getMessages(interaction.guild.id)
        #             message = splitMessage(messages["scrimRegistration"], interaction.guild.id)
        #             message_split = message.split("\n")
        #             title = message_split[0]
        #             description = '\n'.join(message_split[1:])

        #             embed = nextcord.Embed(title=title, description=description, color=White)
        #             await channel.send(embed=embed)
                
        #         else:
        #             embed = nextcord.Embed(title="Scrim Registration", description="Scrim Registration Channel not set. Please set it up using `/setup`", color=Red)
        #             channel = interaction.guild.get_channel(channels["scrimLogChannel"])
        #             await channel.send(embed=embed)
                
        #         channel = interaction.guild.get_channel(channels["scrimLogChannel"])
        #         embed = nextcord.Embed(title=f"{name} has been Scheduled", description=f"{name} was scheduled for {formatted_time}\n `Maps: {map1} & {map2}`\n`Selection Mode: {selection_mode}`", color=Green)
        #         embed.set_footer(text=f"Scheduled at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC by @{interaction.user.name}")
        #         await channel.send(embed=embed)

        #         formatOutput(output=f"   {name} has been scheduled | Maps: {map1} & {map2} | Mode: {selection_mode}", status="Good", guildID=guildID)

        # except Exception as e:
        #     error_traceback = traceback.format_exc()
        #     await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_schedule_Cog(bot))