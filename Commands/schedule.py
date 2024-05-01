import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getChannels, getMessages, splitMessage, getScrims
from Keys import DB
from BotData.colors import *
from BotData.mapdata import *

class NamingView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, scrims):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.scrims = scrims

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
                    await interaction.response.send_modal(modal=NamingModal(interaction, self.scrims))

                elif custom_id == "cancel":
                    embed = nextcord.Embed(title="Scrim Scheduling // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class NamingModal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction, scrims):
        super().__init__(title="Scrim Name", timeout=None)
        self.interaction = interaction
        self.scrims = scrims

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
            name_used = False

            for scrim in self.scrims:
                if self.input.value == scrim["scrimName"]:
                    name_used = True
            
            if name_used == True:
                embed = nextcord.Embed(title="Scrim Scheduling // Name Taken", description="This name is already in use, please choose another", color=Red)
                await interaction.response.edit_message(embed=embed, view=NamingView(interaction, self.scrims))

            else: 
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

            if 'map_2' not in self.schedule_data: self.schedule_data["map_2"] = None # No map 2

            embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Team Type", description="Select the team type for the scrim", color=White)
            await interaction.response.edit_message(embed=embed, view=TeamTypeView(interaction, self.schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class TeamTypeView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        trios_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Trios")
        trios_button.callback = self.create_callback("Trios")
        self.add_item(trios_button)

        duos_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Duos")
        duos_button.callback = self.create_callback("Duos")
        self.add_item(duos_button)

        solos_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Solos")
        solos_button.callback = self.create_callback("Solos")
        self.add_item(solos_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("Cancel")
        self.add_item(cancel_button)

    def create_callback(self, team_type):
        async def callback(interaction: nextcord.Interaction):
            try:
                if team_type != "Cancel":
                    self.schedule_data["team_type"] = team_type

                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Max Teams", description="How many teams will be participating in the scrim?\nAny teams that sign up over this limit will become reserve teams", color=White)
                    await interaction.response.edit_message(embed=embed, view=MaxTeamView(interaction, self.schedule_data))

                else:
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class MaxTeamView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data
        self.add_item(MaxTeamsDropdown(interaction, schedule_data))

class MaxTeamsDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        self.interaction = interaction
        self.schedule_data = schedule_data

        options = []
        if self.schedule_data["team_type"] == "Trios": 
            for number in range(20, 4, -1):
                options.append(nextcord.SelectOption(label=str(number), value=str(number)))

        else:
            for number in range(30, 9, -1):
                options.append(nextcord.SelectOption(label=str(number), value=str(number)))

        super().__init__(placeholder="Select Max Teams", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            max_teams = interaction.data["values"][0]
            self.schedule_data["max_teams"] = int(max_teams)

            embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Total Games", description="How many games will be played in the scrim?", color=White)
            await interaction.response.edit_message(embed=embed, view=TotalGamesView(interaction, self.schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class TotalGamesView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data
        self.add_item(TotalGamesDropdown(interaction, schedule_data))

class TotalGamesDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        self.interaction = interaction
        self.schedule_data = schedule_data

        options = []
        for number in range(10, 1, -1):
            options.append(nextcord.SelectOption(label=str(number), value=str(number)))

        super().__init__(placeholder="Select Total Games", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            total_games = interaction.data["values"][0]
            self.schedule_data["total_games"] = int(total_games)

            embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Interval Setup", description="Is this scrim recurring?", color=White)
            await interaction.response.edit_message(embed=embed, view=IntervalView(interaction, self.schedule_data))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

class IntervalView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        yes_button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="Yes")
        yes_button.callback = self.create_callback("Yes")
        self.add_item(yes_button)

        no_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="No")
        no_button.callback = self.create_callback("No")
        self.add_item(no_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("Cancel")
        self.add_item(cancel_button)

    def create_callback(self, action):
        async def callback(interaction: nextcord.Interaction):
            try:
                if action == "Yes":
                    self.schedule_data["interval"] = True
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Interval Setup", description="How long is the interval between each scrim?", color=White)
                    await interaction.response.edit_message(embed=embed, view=IntervalTimeView(interaction, self.schedule_data))

                elif action == "No":
                    self.schedule_data["interval"] = False

                    if self.schedule_data['map_2'] == None: 
                        embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Confirmation", description=f"Confirm Scheduling of: **{self.schedule_data['scrim_name']}**\n\nTime: <t:{self.schedule_data['scrim_time']}:f> (**{self.schedule_data['scrim_time']}**)\nMap: **{self.schedule_data['map_1']}**\nPOI Selection Mode: **{self.schedule_data['poi_selection_mode']}**\nTeam Type: **{self.schedule_data['team_type']}**\nMax Teams: **{self.schedule_data['max_teams']}**\nTotal Games: **{self.schedule_data['total_games']}**\nInterval: **{self.schedule_data['interval']}**", color=White)
                    else: 
                        embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Confirmation", description=f"Confirm Scheduling of: **{self.schedule_data['scrim_name']}**\n\nTime: <t:{self.schedule_data['scrim_time']}:f> (**{self.schedule_data['scrim_time']}**)\nMaps: **{self.schedule_data['map_1']}** & **{self.schedule_data['map_2']}**\nPOI Selection Mode: **{self.schedule_data['poi_selection_mode']}**\nTeam Type: **{self.schedule_data['team_type']}**\nMax Teams: **{self.schedule_data['max_teams']}**\nTotal Games: **{self.schedule_data['total_games']}**\nInterval: **{self.schedule_data['interval']}**", color=White)

                    await interaction.response.edit_message(embed=embed, view=ConfirmationView(interaction, self.schedule_data))

                elif action == "Cancel":
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class IntervalTimeView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, schedule_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.schedule_data = schedule_data

        daily_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Daily")
        daily_button.callback = self.create_callback("Daily")
        self.add_item(daily_button)

        weekly_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Weekly")
        weekly_button.callback = self.create_callback("Weekly")
        self.add_item(weekly_button)

        fortnightly_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Fortnightly")
        fortnightly_button.callback = self.create_callback("Fortnightly")
        self.add_item(fortnightly_button)

        monthly_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Monthly")
        monthly_button.callback = self.create_callback("Monthly")
        self.add_item(monthly_button)

        cancel_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Cancel")
        cancel_button.callback = self.create_callback("cancel")
        self.add_item(cancel_button)

    def create_callback(self, interval):
        async def callback(interaction: nextcord.Interaction):
            try:
                if interval != "cancel":
                    self.schedule_data["recurrence"] = interval

                    if self.schedule_data['map_2'] == None: 
                        embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Confirmation", description=f"Confirm Scheduling of: **{self.schedule_data['scrim_name']}**\n\nTime: <t:{self.schedule_data['scrim_time']}:f> (**{self.schedule_data['scrim_time']}**)\nMap: **{self.schedule_data['map_1']}**\nPOI Selection Mode: **{self.schedule_data['poi_selection_mode']}**\nTeam Type: **{self.schedule_data['team_type']}**\nMax Teams: **{self.schedule_data['max_teams']}**\nTotal Games: **{self.schedule_data['total_games']}**\nInterval: **{self.schedule_data['interval']}**\nRecurrence: **{self.schedule_data['recurrence']}**", color=White)
                    else: 
                        embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Confirmation", description=f"Confirm Scheduling of: **{self.schedule_data['scrim_name']}**\n\nTime: <t:{self.schedule_data['scrim_time']}:f> (**{self.schedule_data['scrim_time']}**)\nMaps: **{self.schedule_data['map_1']}** & **{self.schedule_data['map_2']}**\nPOI Selection Mode: **{self.schedule_data['poi_selection_mode']}**\nTeam Type: **{self.schedule_data['team_type']}**\nMax Teams: **{self.schedule_data['max_teams']}**\nTotal Games: **{self.schedule_data['total_games']}**\nInterval: **{self.schedule_data['interval']}**\nRecurrence: **{self.schedule_data['recurrence']}**", color=White)

                    await interaction.response.edit_message(embed=embed, view=ConfirmationView(interaction, self.schedule_data))

                else:
                    embed = nextcord.Embed(title=f"Scrim Scheduling: {self.schedule_data['scrim_name']} // Scrim Scheduling Cancelled", description="Scrim Scheduling has been cancelled", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)
            
            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

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

                    dateandtime = datetime.datetime.fromtimestamp(int(self.schedule_data["scrim_time"]))
                    discord_time = dateandtime.astimezone(datetime.timezone.utc)
                    formatted_time = nextcord.utils.format_dt(dateandtime, "f")

                    try: # Create Event
                        #image = ""
                        await interaction.guild.create_scheduled_event(
                            name=self.schedule_data['scrim_name'], 
                            description="Scrim Scheduled by Scrimotron", 
                            entity_type=nextcord.ScheduledEventEntityType.external, 
                            metadata=nextcord.EntityMetadata(location=interaction.guild.name),
                            start_time=discord_time,
                            end_time=discord_time + datetime.timedelta(hours=3),
                            privacy_level=nextcord.ScheduledEventPrivacyLevel.guild_only, 
                            reason="Scrim Scheduled by Scrimotron"
                            #image=image #Breaks due to limitations in discord API. Images have to be local files not URLs, Potential fix/workaround later?
                            )
                        
                        # Calculate Next Interval
                        if self.schedule_data["interval"] == True:
                            if self.schedule_data["recurrence"] == "Daily": next_interval = 86400
                            elif self.schedule_data["recurrence"] == "Weekly": next_interval = 604800
                            elif self.schedule_data["recurrence"] == "Fortnightly": next_interval = 1209600
                            elif self.schedule_data["recurrence"] == "Monthly": next_interval = 2419200

                            self.schedule_data["next_interval"] = self.schedule_data["scrim_time"] + next_interval

                        # Save Scrim
                        DB[str(command["guildID"])]["ScrimData"].insert_one({
                            "scrimName": self.schedule_data['scrim_name'],
                            "scrimEpoch": self.schedule_data['scrim_time'],

                            "scrimConfiguration": {
                                "maxTeams": self.schedule_data['max_teams'],
                                "teamType": self.schedule_data['team_type'],
                                "poiSelectionMode": self.schedule_data['poi_selection_mode'],
                                "totalGames": self.schedule_data['total_games'],
                                "open": {
                                    "checkin": False,
                                    "poi": False
                                },
                                "complete" : {
                                    "poi": False,
                                    "checkin": False,
                                    "setup": False
                                },
                                "interval": {
                                    "repeating": self.schedule_data['interval'],
                                    "interval": self.schedule_data['recurrence'],
                                    "next": self.schedule_data['next_interval']
                                },
                                "maps": {
                                    "map1": self.schedule_data['map_1'],
                                    "map2": self.schedule_data['map_2']
                                },
                                "IDs": {
                                    "vcCategory": None,
                                    "discordEvent": None
                                }},
                            
                            "scrimTeams": {

                            }
                            })

                        embed = nextcord.Embed(title=f"Scrim Scheduled: {self.schedule_data['scrim_name']} // Scheduled", description=f"**{self.schedule_data['scrim_name']}** Has been Scheduled\n\nTime: <t:{self.schedule_data['scrim_time']}:f> (**{self.schedule_data['scrim_time']}**)\nMaps: **{self.schedule_data['map_1']}** & **{self.schedule_data['map_2']}**\nPOI Selection Mode: **{self.schedule_data['poi_selection_mode']}**", color=White)
                        await interaction.edit_original_message(embed=embed)
                        
                        channels = getChannels(command['guildID'])
                        if channels["scrimRegistrationChannel"] != None:
                            channel = interaction.guild.get_channel(channels["scrimRegistrationChannel"])

                            messages = getMessages(interaction.guild.id)
                            message = splitMessage(messages["scrimRegistration"], interaction.guild.id)

                            embed = nextcord.Embed(title=message[0], description=message[1], color=White)
                            await channel.send(embed=embed)
                        
                        else:
                            embed = nextcord.Embed(title="Scrim Registration", description="Scrim Registration Channel not set. Please set it up using `/setup`", color=Red)
                            channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                            await channel.send(embed=embed)
                        
                        channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                        embed = nextcord.Embed(title=f"{self.schedule_data['scrim_name']} has been Scheduled", description=f"{self.schedule_data['scrim_name']} was scheduled for {formatted_time}\nMaps: **{self.schedule_data['map_1']}** & **{self.schedule_data['map_2']}**\nPOI Selection Mode: **{self.schedule_data['poi_selection_mode']}**", color=Green)
                        embed.set_footer(text=f"Scheduled at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC by @{interaction.user.name}")
                        await channel.send(embed=embed)

                        formatOutput(output=f"   {self.schedule_data['scrim_name']} has been scheduled", status="Good", guildID=command["guildID"])

                    except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

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

        scrims = getScrims(command["guildID"])
        if len(scrims) >= 7: # Schedule Limit
            embed = nextcord.Embed(title="Scrim Scheduling // Error", description="You can only have up to 5 scrims scheduled at a time", color=Red)
            await interaction.edit_original_message(embed=embed)

        else:
            embed = nextcord.Embed(title="Scrim Scheduling // Name your Scrim", description="What would you like to name your Scrim?", color=White)
            await interaction.edit_original_message(embed=embed, view=NamingView(interaction, scrims))

def setup(bot):
    bot.add_cog(Command_schedule_Cog(bot))