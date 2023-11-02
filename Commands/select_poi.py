import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_poi
from Config import db_team_data, db_bot_data

### POIS (as of season 18)
worlds_edge_pois = [
'Big Maude',
'Climatizer',
'Countdown',
'Fragment East',
'Harvester',
'Landslide',
'Launch Site',
'Lava Fissure',
'Lava Siphon', 
'Mirage Voyage',
'Monument',
'Overlook',
'Skyhook',
'Stacks',
'Staging',
'Survey Camp',
'The Dome',
'The Epicenter',
'The Geyser',
'The Tree',
'Thermal Station',
'Trials'
]
olympus_pois = [
'Bonsai Plaza',
'Clinc',
'Docks',
'Elysium',
'Energy Depot',
'Estates',
'Fight Night',
'Gardens',
'Grow Towers',
'Hammond Labs',
'Hydroponics',
'Icarus',
'Oasis',
'Orbial Cannon',
'Phase Driver',
'Power Grid',
'Rift',
'Solar Array',
'Supercarrier',
'Terminal',
'Turbine'
]
kings_canyon_pois = [
'Airbase',
'Artillery',
'Basin',
'Bunker',
'Capacitor',
'Caustic Treatment',
'Containment',
'Crash Site',
'Gauntlet',
'Hydro',
'Map Room',
'Market',
'Relic',
'Repulsor',
'Rig',
'Runoff',
'Singh Labs',
'Spotted Lakes',
'Swamps',
'The Cage',
'The Pit',
]
storm_point_pois = [
'Barometer',
'Cascade Falls',
'Cenote Cave',
'Ceto Station',
'Checkpoint',
'Command Center',
'Devastaded Coast',
'Downed Beast',
'Echo HQ',
'Launch Pad',
'Lighting Rod',
'North Pad',
'Ship Fall',
'Storm Catcher',
'The Mill',
'The Pylon',
'The Wall',
'Zeus Station'
]
broken_moon_pois = [ # Soon

]

class Command_select_poi_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    class select_poi_map2_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            map2 = db_bot_data.find_one({"maps": {"$exists": True}})["maps"]["map2"]
            data = list(db_team_data.find())
            picked_pois = []
            for i in data:
                if i["pois"]["map2"] != "None":
                    picked_pois.append(i["pois"]["map2"])
                    
            if map2 == "Worlds Edge":
                for i in worlds_edge_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map2 == "Olympus":
                for i in olympus_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map2 == "Kings Canyon":
                for i in kings_canyon_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map2 == "Storm Point":
                for i in storm_point_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map2 == "Broken Moon":
                for i in broken_moon_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)

        def create_callback(self, label):
            async def callback(interaction: nextcord.Interaction):
                try:
                    maps = db_bot_data.find_one({"maps": {"$exists": True}})
                    map1 = maps["maps"]["map1"]
                    map2 = maps["maps"]["map2"]
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": label}})
                    data = db_team_data.find_one({"team_name": self.team_name})
                    channel = interaction.guild.get_channel(channel_poi)
                    try: # check if team is repicking pois
                        messages = await channel.history(limit=30).flatten()
                        for msg in messages:
                            if msg.author.bot:
                                if msg.embeds[0].title == f"POIs Picked for {self.team_name}":
                                    await msg.delete()
                    except: pass # nothing found
                    finally: # send poi selection
                        embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=f"{map1} - {data['pois']['map1']}\n{map2} - {data['pois']['map2']}", color=0x000)
                        channel = interaction.guild.get_channel(channel_poi)
                        await channel.send(embed=embed)
                        embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=0x000)
                        await interaction.send(embed=embed, ephemeral=True)
                    formatOutput(output=f"   /select_poi | {self.team_name} has selected {map1} - {data['pois']['map1']} & {map2} - {data['pois']['map2']}", status="Good")
                    formatOutput(output=f"   /select_poi was successful!", status="Good")
                except Exception as e:
                    await errorResponse(error=e, command="select_poi", interaction=interaction)
            return callback

    class select_poi_map1_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name 
            map1 = db_bot_data.find_one({"maps": {"$exists": True}})["maps"]["map1"]
            data = list(db_team_data.find())
            picked_pois = []
            for i in data:
                if i["pois"]["map1"] != "None":
                    picked_pois.append(i["pois"]["map1"])
                    
            if map1 == "Worlds Edge":
                for i in worlds_edge_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map1 == "Olympus":
                for i in olympus_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map1 == "Kings Canyon":
                for i in kings_canyon_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map1 == "Storm Point":
                for i in storm_point_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)
            
            elif map1 == "Broken Moon":
                for i in broken_moon_pois:
                    if i not in picked_pois:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else:
                        button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)

                    button.callback = self.create_callback(i)    
                    self.add_item(button)

        def create_callback(self, label):
            async def callback(interaction: nextcord.Interaction):
                try:
                    maps = db_bot_data.find_one({"maps": {"$exists": True}})
                    map1 = maps["maps"]["map1"]
                    map2 = maps["maps"]["map2"]
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": label}})
                    embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nBlue Buttons indicate that a team has picked that POI", color=0x000)
                    embed.set_footer(text=f"Current Picks: {map1} - {label}")
                    await interaction.response.send_message(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)
                except Exception as e:
                    await errorResponse(error=e, command="select_poi", interaction=interaction)
            return callback

    @nextcord.slash_command(guild_ids=[guildID], name="select_poi", description="Select POIs")
    async def select_poi(self, interaction: nextcord.Interaction, team_name: str):
        command = 'select_poi'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.response.defer(ephemeral=True)

        try:
            data = list(db_team_data.find())
            if db_bot_data.find_one({"maps": {"$exists": True}}) == None:
                await interaction.edit_original_message(content="POI Selections are not open yet!")
                formatOutput(output=f"   /{command} | POI Selections are not open yet!", status="Warning")
            else:
                try:
                    if db_team_data.find_one({"team_name": team_name}) != None: # team exists
                        data = db_team_data.find_one({"team_name": team_name})
                        if interaction.user.id == data["captain"]: # user is captain
                            maps = db_bot_data.find_one({"maps": {"$exists": True}})
                            map1 = maps["maps"]["map1"]
                            map2 = maps["maps"]["map2"]
                            embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map1}\nGray Buttons indicate no team has chosen that POI yet,\nBlue Buttons indicate that a team has picked that POI", color=0x000)
                            await interaction.edit_original_message(embed=embed, view=Command_select_poi_Cog.select_poi_map1_view(interaction, team_name))
                        else: # not captain
                            if interaction.user.guild_permissions.administrator: # is admin
                                maps = db_bot_data.find_one({"maps": {"$exists": True}})
                                map1 = maps["maps"]["map1"]
                                map2 = maps["maps"]["map2"]
                                embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map1}\nGray Buttons indicate no team has chosen that POI yet,\nBlue Buttons indicate that a team has picked that POI", color=0x000)
                                await interaction.edit_original_message(embed=embed, view=Command_select_poi_Cog.select_poi_map1_view(interaction, team_name))
                            else: # not admin
                                await interaction.edit_original_message(content=f"You are not the captain of {team_name}!")
                                formatOutput(output=f"   /{command} | {userID} is not captain of {team_name}!", status="Warning")
                    else: # team doesnt exist
                        await interaction.edit_original_message(content=f"Team {team_name} not found!")
                        formatOutput(output=f"   /{command} | {team_name} not found!", status="Warning")
                except Exception as e:
                    await errorResponse(error=e, command=command, interaction=interaction)
        except Exception as e:
            await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_select_poi_Cog(bot))