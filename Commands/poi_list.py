import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getTeams, getScrims, getScrim
from BotData.mapdata import MapData
from BotData.colors import *

class MainView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, scrims, filter):
        super().__init__(timeout=None)
        self.add_item(MainDropdown(interaction, scrims, filter))

class MainDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, scrims, filter):
        self.interaction = interaction
        self.scrims = scrims
        self.filter = filter

        options = []

        for scrim in scrims: options.append(nextcord.SelectOption(label=scrim["scrimName"], value=scrim["scrimName"]))

        super().__init__(placeholder="Select a Scrim", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        message = []
        try:
            teams = getTeams(interaction.guild.id, interaction.data["values"][0])
            scrim = getScrim(interaction.guild.id, interaction.data["values"][0])
            max_teams = getScrim(interaction.guild.id, interaction.data["values"][0])["scrimConfiguration"]["maxTeams"]
            team_count = 0
            maps = scrim["scrimConfiguration"]["maps"]
            map_number = 1

            if scrim['scrimConfiguration']['poiSelectionMode'] != "No POIs":
                mode = scrim['scrimConfiguration']['poiSelectionMode']

                for map in maps:
                    if map == None:
                        map_number += 1
                        continue
                    message.append(f"\n**{maps[map]}**")

                    if self.filter == "Selections":
                        for team, data in teams.items():
                            if mode == "ALGS": message.append(f"{team_count+1} | **{data['teamName']}@{data['teamPois'][f'map{map_number}'][f'map{map_number}ID']}** - {data['teamPois'][f'map{map_number}'][f'map{map_number}POI']}")
                            else: message.append(f"{team_count+1} | **{data['teamName']}** - {data['teamPois'][f'map{map_number}'][f'map{map_number}POI']}")
                            team_count += 1

                            if team_count == max_teams: message.append("**-------------------RESERVES BELOW-------------------**")

                    # elif self.filter == "POI List" or self.filter == "None":
                    #     for name, data in MapData[f"{scrim['scrimConfiguration']['maps'][f'map{map_number}']}"].items():
                    #         if mode == "ALGS":
                    #             if data['ID'] != None: message.append(f"{name} | @{data['ID']}")
                    #             else: continue

                    #         elif mode == "Simple": message.append(name)

                    #         team_count += 1

                    #     if self.filter == "POI List": # Add contests & sort
                    #         if mode == "ALGS": message.sort(key=lambda x: int(x.split("@")[1])) # Sort by ALGS @ID
                    #         else: message.sort() # Sort alphabetically for simple pois

                embed = nextcord.Embed(title=f"POI List - {interaction.data["values"][0]} - Filter: {self.filter}", description='\n'.join(message), color=White)
                embed.set_footer(text=f"Filtered By: {self.filter}")
                await interaction.followup.edit_message(interaction.message.id, embed=embed)

            else: # No POIs
                embed = nextcord.Embed(title=f"POI List - {interaction.data["values"][0]} - Filter: {self.filter}", description="POIs are not being chosen for this scrim", color=Yellow)
                await interaction.followup.edit_message(interaction.message.id, embed=embed)

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

class Command_poi_list_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="poi_list", description="Shows a list of all POIs filters can be used")
    async def poi_list(self, interaction: nextcord.Interaction,
        filter = nextcord.SlashOption(name="filter", description="Select a filter", choices=["Selections"], required=True)):

        global command
        command = {"name": interaction.application_command.name, "userID": interaction.user.id, "guildID": interaction.guild.id}
        formatOutput(output=f"/{command['name']} Used by {command['userID']} | @{interaction.user.name}", status="Normal", guildID=command["guildID"])

        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        try:
            scrims = getScrims(command["guildID"])
            if len(scrims) == 0: # No Scrims
                embed = nextcord.Embed(title=f"POI List - Filter: {filter}", description="No scrims have been scheduled\nSchedule a scrim using `/schedule`", color=Yellow)
                await interaction.edit_original_message(embed=embed)
                return

            else: # 1 or more scrims
                embed = nextcord.Embed(title=f"POI List - Filter: {filter}", description="Use the dropdown below to select a scrim to view POIs for", color=White)
                embed.set_footer(text="Filtering may take some time to process")
                await interaction.edit_original_message(embed=embed, view=MainView(interaction, scrims, filter))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

def setup(bot):
    bot.add_cog(Command_poi_list_Cog(bot))