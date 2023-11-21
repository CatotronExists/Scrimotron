import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_poi
from Config import db_team_data, db_bot_data

### POIS (as of season 19)
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
'Storm Catcher',
'The Mill',
'The Pylon',
'The Wall',
'Zeus Station'
]
broken_moon_pois = [ # Soon

]

# POIs often picked together
dual_pois = {
"Worlds Edge": {
    "Mirage Voyage": "Staging",
    "Staging": "Mirage Voyage",
    "Epicenter": "Survey Camp",
    "Survey Camp": "Epicenter",
    "Big Maude": "Stacks",
    "Stacks": "Big Maude",
    "Trials": "Skyhook",
    "Skyhook": "Trials"
},
"Olympus": {
    "Soon": "Soon"
},
"Kings Canyon": {
    "Soon": "Soon"
},
"Storm Point": {
    "Soon": "Soon"
},
"Broken Moon": {
    "Soon": "Soon"
}
}

class Command_select_poi_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class dual_poi_pick_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi, partnered_poi, map):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi
            self.partnered_poi = partnered_poi
            self.map = map
        
        @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)
        async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            poi = f"{self.poi} / {self.partnered_poi}"
            await self.create_callback(poi, self.map)(interaction)

        @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)
        async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            poi = self.poi
            await self.create_callback(poi, self.map)(interaction)    

        def create_callback(self, poi, map):
            async def callback(interaction: nextcord.Interaction):
                try:
                    if map == map1:
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": poi}})
                        embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nBlue Buttons indicate that a team has picked that POI", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)
                    elif map == map2:
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": poi}})
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

    class select_poi_map2_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name

            data = list(db_team_data.find())
            picked_pois = []
            for i in data:
                if i["pois"]["map2"] != "None":
                    if i["team_name"] != self.team_name: # if team is not the current team
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

        def create_callback(self, i):
            async def callback(interaction: nextcord.Interaction):
                try:
                    try: 
                        if dual_pois[map2][i] != None: # is a dual poi
                            dual = True
                    except KeyError: dual = False
                    if dual == True:
                        poi = i
                        partnered_poi = dual_pois[map1][i]
                        embed = nextcord.Embed(title=f"{poi} is usually picked with {partnered_poi}, would you also like to pick {partnered_poi}?", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.dual_poi_pick_view(interaction, self.team_name, poi, partnered_poi, map=map2), ephemeral=True)
                    else: # is not a dual poi
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": i}})
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

            data = list(db_team_data.find())
            picked_pois = []
            for i in data:
                if i["pois"]["map1"] != "None": # if team has picked a poi
                    if i["team_name"] != self.team_name: # if team is not the current team
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
            async def callback(interaction: nextcord.Interaction): ### MAP2 IS BROKEN
                poi = label
                try:
                    try: 
                        if dual_pois[map1][label] != None: # is a dual poi
                            dual = True
                    except KeyError: dual = False # is not a dual poi
                    if dual == True:
                        partnered_poi = dual_pois[map1][label]
                        embed = nextcord.Embed(title=f"{poi} is usually picked with {partnered_poi}, would you also like to pick {partnered_poi}?", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.dual_poi_pick_view(interaction, self.team_name, poi, partnered_poi, map=map1), ephemeral=True)
                    else:
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": poi}})
                        embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nBlue Buttons indicate that a team has picked that POI", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)
                except Exception as e:
                    await errorResponse(error=e, command="select_poi", interaction=interaction)
            return callback

    @nextcord.slash_command(guild_ids=[guildID], name="select_poi", description="Select POIs")
    async def select_poi(self, interaction: nextcord.Interaction, team_name: str):
        command = 'select_poi'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        try: await interaction.response.defer(ephemeral=True)
        except: pass

        try:             
            if db_bot_data.find_one({"poi": {"$exists": True}}) == None: # checking if poi selection is open
                await interaction.edit_original_message(content="POI Selections are not open yet!")
                formatOutput(output=f"   /{command} | POI Selections are not open yet!", status="Warning") 
            else: # -> yes          
                if db_team_data.find_one({"team_name": team_name}) != None: # team exists
                    data = db_team_data.find_one({"team_name": team_name})
                    if interaction.user.id == data["captain"] or interaction.user.guild_permissions.administrator: # user is captain or admin
                        maps = db_bot_data.find_one({"maps": {"$exists": True}})
                        global map1, map2
                        map1 = maps["maps"]["map1"]
                        map2 = maps["maps"]["map2"]
                        embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map1}\nGray Buttons indicate no team has chosen that POI yet,\nBlue Buttons indicate that a team has picked that POI", color=0x000)
                        await interaction.edit_original_message(embed=embed, view=Command_select_poi_Cog.select_poi_map1_view(interaction, team_name))
                    else: # not captain or admin
                        await interaction.edit_original_message(content=f"You are not the captain of {team_name}!")
                        formatOutput(output=f"   /{command} | {userID} is not captain of {team_name}!", status="Warning")
                else: # team doesnt exist
                    await interaction.edit_original_message(content=f"Team {team_name} not found!")
                    formatOutput(output=f"   /{command} | {team_name} not found!", status="Warning")
        except Exception as e:
            await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_select_poi_Cog(bot))