import nextcord
import traceback
import datetime
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getConfigData, getChannels, getTeams, getScrimSetup, getScrimInfo, DB
from BotData.mapdata import MapData
from BotData.colors import *

class TeamPicker(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.add_item(TeamDropdown(self, interaction))

class TeamDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction):
        self.interaction = interaction
        super().__init__(
            placeholder="Select Team",
            min_values=1,
            max_values=1,
            options=[nextcord.SelectOption(label=i, value=i) for i in getTeams(int(interaction.guild.id))],
            custom_id="team_select"
        )

    async def callback(self, interaction: nextcord.Interaction):
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        team_name = interaction.data["values"][0]
        scrim_setup = getScrimSetup(guildID)
        try:
            team = DB[str(guildID)]["TeamData"].find_one({"teamName": team_name})
            if team["teamCaptain"] == userID: # captain check
                if scrim_setup["poiSelectionMode"] == "Simple": description = f"Select a POI for Map 1\nSelection Mode: {scrim_setup['poiSelectionMode']} - Pick one POI per map\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI"
                elif scrim_setup["poiSelectionMode"] == "Advanced": description = f"Select a POI for Map 1\nSelection Mode: {scrim_setup['poiSelectionMode']} - Option to pick Secondary POIs and Tridents\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI"
                embed = nextcord.Embed(title="POI Selection", description=description, color=White)
                await interaction.edit_original_message(embed=embed, view=select_poi_map1_view(interaction, team_name))

            else:
                embed = nextcord.Embed(title="POI Selection", description="POI Selections can only be done by the team captain!", color=Red)
                await interaction.edit_original_message(embed=embed)
                formatOutput(output=f"   /{command} | {userID} is not captain of {team_name}!", status="Warning", guildID=guildID)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

class select_poi_map2_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, team_name):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.team_name = team_name

        team_data = getTeams(int(interaction.guild.id))
        scrim_setup = getScrimSetup(int(interaction.guild.id))
        config_data = getConfigData(int(interaction.guild.id))
        picked_pois = []
        contests = 0
        for team in team_data: # Get all picked pois
            if team["teamPois"]["map2"]["map2POI"] != None: # if team has picked a poi
                if team["teamName"] != self.team_name: # if team is not the current team
                    picked_pois.append(team["teamPois"]["map2"]["map2POI"])

        for poi in picked_pois: # Calculate contests (count)
            if picked_pois.count(poi) > 1: contests = contests + 1

        for poi in MapData[f"{scrim_setup['maps']['map2']}"]:
            if poi not in picked_pois: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.gray)
            else:
                if config_data["maxContests"] != None: # if maxContests is enabled
                    if contests > config_data["maxContests"]: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.red, disabled=True)
                else: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.red)

            button.callback = self.create_callback(poi, scrim_setup)
            self.add_item(button)

    def create_callback(self, label, scrim_setup):
        async def callback(interaction: nextcord.Interaction):
            poi = label
            channels = getChannels(int(interaction.guild.id))
            try:
                if scrim_setup["poiSelectionMode"] == "Simple": # Simple Selection
                    DB[int(interaction.guild.id)]["TeamData"].update_one({"teamName": self.team_name}, {"$set": {"teamPois.map2.map2POI": poi}})

                    message = DB[int(interaction.guild.id)]["TeamData"].find_one({"teamName": self.team_name})["teamSetup"]["poiMessageID"]
                    channel = interaction.guild.get_channel(channels["scrimPoiChannel"])

                    if message != None: # Delete previous poi selection message (if exists)
                        try:
                            message = await interaction.guild.get_channel(channels["scrimPoiChannel"]).fetch_message(message)
                            await message.delete()
                        except: pass

                    # send poi selection
                    team = DB[int(interaction.guild.id)]["TeamData"].find_one({"teamName": self.team_name})
                    embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=f"{map1} - {team['teamPois']['map1POI']}\n{map2} - {team['teamPois']['map2POI']}", color=White)
                    channel = interaction.guild.get_channel(channels["scrimPoiChannel"])
                    await channel.send(embed=embed)
                    embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=White)
                    await interaction.send(embed=embed, ephemeral=True)
                    formatOutput(output=f"   /select_poi | {self.team_name} has selected {map1} - {team['teamPois']['map1POI']} & {map2} - {team['teamPois']['map2POI']}", status="Good", guildID=interaction.guild.id)
                    formatOutput(output=f"   /select_poi was successful!", status="Good", guildID=interaction.guild.id)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
            return callback

class select_poi_map1_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, team_name):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.team_name = team_name

        team_data = getTeams(int(interaction.guild.id))
        scrim_setup = getScrimSetup(int(interaction.guild.id))
        config_data = getConfigData(int(interaction.guild.id))
        picked_pois = []
        contests = 0
        for team in team_data: # Get all picked pois
            if team["teamPois"]["map1"]["map1POI"] != None: # if team has picked a poi
                if team["teamName"] != self.team_name: # if team is not the current team
                    picked_pois.append(team["teamPois"]["map1"]["map1POI"])

        for poi in picked_pois: # Calculate contests (count)
            if picked_pois.count(poi) > 1: contests = contests + 1

        for poi in MapData[f"{scrim_setup['maps']['map1']}"]:
            if poi not in picked_pois: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.gray)
            else:
                if config_data["maxContests"] != None: # if maxContests is enabled
                    if contests > config_data["maxContests"]: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.red, disabled=True)
                else: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.red)

            button.callback = self.create_callback(poi, scrim_setup)
            self.add_item(button)

    def create_callback(self, label, scrim_setup):
        async def callback(interaction: nextcord.Interaction):
            poi = label
            try:
                if scrim_setup["poiSelectionMode"] == "Simple": # Simple Selection
                    DB[int(interaction.guild.id)]["TeamData"].update_one({"teamName": self.team_name}, {"$set": {"teamPois.map1.map1POI": poi}})
                    embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI", color=White)
                    await interaction.send(embed=embed, view=select_poi_map2_view(interaction, self.team_name), ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
            return callback

class Command_select_poi_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="select_poi", description="Select POI(s) for your team")
    async def select_poi(self, interaction: nextcord.Interaction):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        try:
            config_data = getConfigData(guildID)
            scrim_setup = getScrimSetup(guildID)
            scrim_info = getScrimInfo(guildID)
            if config_data["togglePoi"] == True: # poi selection is enabled
                if scrim_setup["poiSelectionOpen"] == True: # poi selection has opened
                    if scrim_info["scrimEpoch"] < datetime.datetime.now().timestamp(): # scrim has started
                        global map1, map2
                        map1 = scrim_setup["maps"]["map1"]
                        map2 = scrim_setup["maps"]["map2"]
                        embed = nextcord.Embed(title="Select POI", description="Select your team from the menu", color=White)
                        await interaction.response.send_message(embed=embed, view=TeamPicker(interaction), ephemeral=True)

                    else: # scrim has already started
                        embed = nextcord.Embed(title="POI Selection", description="Scrim has already started!", color=Red)
                        await interaction.edit_original_message(embed=embed)
                        formatOutput(output=f"   /{command} | Scrim has already started!", status="Warning", guildID=guildID)

                else: # poi selection has not opened
                    embed = nextcord.Embed(title="POI Selection", description="POI Selections have not opened yet!", color=Red)
                    await interaction.edit_original_message(embed=embed)
                    formatOutput(output=f"   /{command} | POI Selections have not opened yet!", status="Warning", guildID=guildID)

            else: # poi selection is disabled
                embed = nextcord.Embed(title="POI Selection", description="POI Selections are disabled for this scrim!", color=Red)
                await interaction.edit_original_message(embed=embed)
                formatOutput(output=f"   /{command} | POI Selections are disabled!", status="Warning", guildID=guildID)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_select_poi_Cog(bot))