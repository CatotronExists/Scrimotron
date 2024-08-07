import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, DB, getScrims, getScrim, getTeam, getMessages, splitMessage, bot
from BotData.mapdata import MapData
from BotData.colors import *

class RegisterView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        edit_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Edit")
        edit_button.callback = self.create_callback("edit")
        self.add_item(edit_button)

        unregister_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Unregister")
        unregister_button.callback = self.create_callback("unregister")
        self.add_item(unregister_button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            scrim_name = None
            scrims = getScrims(interaction.guild.id)
            for scrim in scrims:
                if scrim['scrimConfiguration']['registrationChannel'] == interaction.channel.id:
                    scrim_name = scrim['scrimName']
                    break

            team = getTeam(interaction.guild.id, scrim_name, interaction.message.embeds[0].title)
            scrim = getScrim(interaction.guild.id, scrim_name)

            try:
                if custom_id == "edit":
                    embed = nextcord.Embed(title="Solo Registrations cannot be edited", description="To edit a solo registration, unregister and register a new team", color=White)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "unregister":
                    if interaction.user.id == team["teamPlayer1"] or interaction.user.guild_permissions.administrator == True:
                        msgindex = DB[str(interaction.guild.id)]["ScrimData"].find_one({"scrimName": scrim_name})["scrimConfiguration"]["registrationMessages"]

                        # Reserve Message Editing
                        if len(msgindex) < scrim['scrimConfiguration']['maxTeams'] - 1: # If there are less than max_teams (-1 to remove unregistered team)
                            if scrim['scrimConfiguration']['reserveMessage'] != None: # and a reserve message exists, delete it
                                reserve_message = await interaction.channel.fetch_message(scrim['scrimConfiguration']['reserveMessage'])
                                await reserve_message.delete()

                                DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim_name}, {"scrimConfiguration.reserveMessage": None})
                                DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim_name}, {"$pull": {"scrimConfiguration.registrationMessages": reserve_message.id}})

                        elif len(msgindex) >= scrim['scrimConfiguration']['maxTeams'] - 1: # If there are max_teams or more (-1 to remove unregistered team)
                            # Then swap first reserve index[max_teams + 1] with index[max_teams] (then delete unregistered team index)
                            # first_reserve refers to the team that was the first reserve | reserve_message refers to the message that was the reserve message
                            reserve_message = await interaction.channel.fetch_message(scrim['scrimConfiguration']['IDs']['reserveMessage']) # Reserve Message
                            first_reserve = await interaction.channel.fetch_message(msgindex[scrim['scrimConfiguration']['maxTeams']+ 1]) # First Reserve

                            reserve_message_raw = splitMessage(getMessages(interaction.guild.id)['scrimReserve'], interaction.guild.id, scrim_name)
                            reserve_message_embed = nextcord.Embed(title=reserve_message_raw[0], description=reserve_message_raw[1], color=White) # Build new reserve message

                            first_reserve_embed = nextcord.Embed(title=first_reserve.embeds[0].title, description=first_reserve.embeds[0].description)
                            if first_reserve.embeds[0].footer != None: first_reserve_embed.set_footer(text=first_reserve.embeds[0].footer.text) # Rebuild first reserve signup

                            DB.Scrimotron.SavedMessages.update_one({"messageID": reserve_message.id}, {"$set": {"messageID": first_reserve.id}}) # Update saved messages

                            new_view = AutomatedRegisterView(interaction=DB.Scrimotron.SavedMessages.find_one({"messageID": first_reserve.id})["interactionID"], type=None, guildID=interaction.guild.id, channelID=interaction.channel.id)

                            first_reserve_id = await reserve_message.edit(embed=first_reserve_embed, view=new_view) # Edit reserve message to first reserve
                            reserve_message_id = await first_reserve.edit(embed=reserve_message_embed, view=None) # Edit first reserve to reserve message

                            DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim_name}, {"$set": {"scrimConfiguration.IDs.reserveMessage": reserve_message_id.id}})
                            DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim_name}, {"$set": {f"scrimTeams.{first_reserve.embeds[0].title}.messageID": first_reserve_id.id}})

                        else: # Nothing happens (no reserves exist yet)
                            pass

                        DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim_name}, {"$unset": {f"scrimTeams.{interaction.message.embeds[0].title}": ""}})
                        DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim_name}, {"$pull": {"scrimConfiguration.registrationMessages": team["messageID"]}})

                        message = await interaction.channel.fetch_message(team["messageID"])
                        await message.delete()
                        formatOutput(output=f"   {interaction.message.embeds[0].title} was unregistered!", status="Good", guildID=interaction.guild.id)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain and Admins can unregister teams!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class AutomatedRegisterView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, type, guildID, channelID):
        super().__init__(timeout=None)
        scrim_name = None
        self.interaction = interaction
        scrims = getScrims(guildID)

        for scrim in scrims:
            if scrim['scrimConfiguration']['registrationChannel'] == channelID:
                scrim_name = scrim['scrimName']
                break
        scrim = getScrim(guildID, scrim_name)

        edit_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Edit")
        edit_button.callback = self.create_callback("edit", scrim)
        self.add_item(edit_button)

        unregister_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Unregister")
        unregister_button.callback = self.create_callback("unregister", scrim)
        self.add_item(unregister_button)

        if type == "checkin" or scrim["scrimConfiguration"]["open"]["checkin"] == True:
            checkin_button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="Check In ✅")
            checkin_button.callback = self.create_callback("checkin", scrim)
            self.add_item(checkin_button)

        if type == "poi" or scrim["scrimConfiguration"]["open"]["poi"] == True:
            poi_button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="POI Selection")
            poi_button.callback = self.create_callback("poi", scrim)
            self.add_item(poi_button)

    def create_callback(self, custom_id, scrim):
        async def callback(interaction: nextcord.Interaction):
            team = getTeam(interaction.guild.id, scrim['scrimName'], interaction.message.embeds[0].title)

            try:
                if custom_id == "edit":
                    if interaction.user.id == team["teamPlayer1"]:
                        embed = nextcord.Embed(title="Run `/register` to edit your signup!", description="The team name and captain of the team must remain the same\n*Signup a new team if you wish to edit captain and or team name*", color=White)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can edit signups!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "unregister":
                    if interaction.user.id == team["teamPlayer1"] or interaction.user.guild_permissions.administrator == True:
                        msgindex = DB[str(interaction.guild.id)]["ScrimData"].find_one({"scrimName": scrim['scrimName']})["scrimConfiguration"]["registrationMessages"]

                        # Reserve Message Editing
                        if len(msgindex) < scrim['scrimConfiguration']['maxTeams'] - 1: # If there are less than max_teams (-1 to remove unregistered team)
                            if scrim['scrimConfiguration']['IDs']['reserveMessage'] != None: # and a reserve message exists, delete it
                                reserve_message = await interaction.channel.fetch_message(scrim['scrimConfiguration']['reserveMessage'])
                                await reserve_message.delete()

                                DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"scrimConfiguration.reserveMessage": None})
                                DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$pull": {"scrimConfiguration.registrationMessages": reserve_message.id}})

                        elif len(msgindex) >= scrim['scrimConfiguration']['maxTeams'] - 1: # If there are max_teams or more (-1 to remove unregistered team)
                            # Then swap first reserve index[max_teams + 1] with index[max_teams] (then delete unregistered team index)
                            # first_reserve refers to the team that was the first reserve | reserve_message refers to the message that was the reserve message
                            reserve_message = await interaction.channel.fetch_message(scrim['scrimConfiguration']['IDs']['reserveMessage']) # Reserve Message
                            first_reserve = await interaction.channel.fetch_message(msgindex[scrim['scrimConfiguration']['maxTeams']+ 1]) # First Reserve

                            reserve_message_raw = splitMessage(getMessages(interaction.guild.id)['scrimReserve'], interaction.guild.id, scrim["scrimName"])
                            reserve_message_embed = nextcord.Embed(title=reserve_message_raw[0], description=reserve_message_raw[1], color=White) # Build new reserve message

                            first_reserve_embed = nextcord.Embed(title=first_reserve.embeds[0].title, description=first_reserve.embeds[0].description)
                            if first_reserve.embeds[0].footer != None: first_reserve_embed.set_footer(text=first_reserve.embeds[0].footer.text) # Rebuild first reserve signup

                            DB.Scrimotron.SavedMessages.update_one({"messageID": reserve_message.id}, {"$set": {"messageID": first_reserve.id}}) # Update saved messages

                            new_view = AutomatedRegisterView(interaction=DB.Scrimotron.SavedMessages.find_one({"messageID": first_reserve.id})["interactionID"], type=None, guildID=interaction.guild.id, channelID=interaction.channel.id)

                            first_reserve_id = await reserve_message.edit(embed=first_reserve_embed, view=new_view) # Edit reserve message to first reserve
                            reserve_message_id = await first_reserve.edit(embed=reserve_message_embed, view=None) # Edit first reserve to reserve message

                            DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$set": {"scrimConfiguration.IDs.reserveMessage": reserve_message_id.id}})
                            DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$set": {f"scrimTeams.{first_reserve.embeds[0].title}.messageID": first_reserve_id.id}})

                        else: # Nothing happens (no reserves exist yet)
                            pass

                        DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$unset": {f"scrimTeams.{interaction.message.embeds[0].title}": ""}})
                        DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$pull": {"scrimConfiguration.registrationMessages": team["messageID"]}})

                        message = await interaction.channel.fetch_message(team["messageID"])
                        await message.delete()
                        formatOutput(output=f"   {interaction.message.embeds[0].title} was unregistered!", status="Good", guildID=interaction.guild.id)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain and Admins can unregister teams!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "checkin":
                    if interaction.user.id == team["teamPlayer1"]:
                        if team["teamStatus"]["checkin"] == False:
                            DB[str(interaction.guild.id)]["TeamData"].update_one({"teamName": interaction.message.embeds[0].title}, {"$set": {"teamStatus.checkin": True}})
                            message = await interaction.channel.fetch_message(team["messageID"])
                            await message.edit(embed=message.embeds[0].set_footer(text="Checked In ✅"))

                            embed = nextcord.Embed(title="Team Checked In", description=f"**{interaction.message.embeds[0].title}** has been checked in for **{scrim["scrimName"]}**", color=Green)
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        else:
                            embed = nextcord.Embed(title="Team Already Checked In", description=f"**{interaction.message.embeds[0].title}** has already checked in!", color=Red)
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can check in!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "poi":
                    if interaction.user.id == team["teamPlayer1"]:
                        if scrim["scrimConfiguration"]["poiSelectionMode"] == "Simple": embed = nextcord.Embed(title=f"Select a POI for Map 1 ({scrim['scrimConfiguration']['maps']['map1']})", description="Selection Mode: Simple - Pick one POI per map\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI")
                        elif scrim["scrimConfiguration"]["poiSelectionMode"] == "Advanced": embed = nextcord.Embed(title=f"Select a POI for Map 1 ({scrim['scrimConfiguration']['maps']['map1']})", description="Selection Mode: Advanced - Option to pick Secondary POIs and Tridents\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI")

                        await interaction.response.send_message(embed=embed, view=POIView(interaction, scrim, team, map_num=1), ephemeral=True)

                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can open POI Selection!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class AutomatedRegisterView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, type, guildID, channelID):
        super().__init__(timeout=None)
        scrim_name = None
        self.interaction = interaction
        scrims = getScrims(guildID)

        for scrim in scrims:
            if scrim['scrimConfiguration']['registrationChannel'] == channelID:
                scrim_name = scrim['scrimName']
                break
        scrim = getScrim(guildID, scrim_name)

        edit_button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label="Edit")
        edit_button.callback = self.create_callback("edit", scrim)
        self.add_item(edit_button)

        unregister_button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label="Unregister")
        unregister_button.callback = self.create_callback("unregister", scrim)
        self.add_item(unregister_button)

        if type == "checkin" or scrim["scrimConfiguration"]["open"]["checkin"] == True:
            checkin_button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="Check In ✅")
            checkin_button.callback = self.create_callback("checkin", scrim)
            self.add_item(checkin_button)

        if type == "poi" or scrim["scrimConfiguration"]["open"]["poi"] == True:
            poi_button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label="POI Selection")
            poi_button.callback = self.create_callback("poi", scrim)
            self.add_item(poi_button)

    def create_callback(self, custom_id, scrim):
        async def callback(interaction: nextcord.Interaction):
            team = getTeam(interaction.guild.id, scrim['scrimName'], interaction.message.embeds[0].title)

            try:
                if custom_id == "edit":
                    if interaction.user.id == team["teamPlayer1"]:
                        embed = nextcord.Embed(title="Run `/register` to edit your signup!", description="The team name and captain of the team must remain the same\n*Signup a new team if you wish to edit captain and or team name*", color=White)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can edit signups!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "unregister":
                    if interaction.user.id == team["teamPlayer1"] or interaction.user.guild_permissions.administrator == True:
                        msgindex = DB[str(interaction.guild.id)]["ScrimData"].find_one({"scrimName": scrim['scrimName']})["scrimConfiguration"]["registrationMessages"]

                        # Reserve Message Editing
                        if len(msgindex) < scrim['scrimConfiguration']['maxTeams'] - 1: # If there are less than max_teams (-1 to remove unregistered team)
                            if scrim['scrimConfiguration']['IDs']['reserveMessage'] != None: # and a reserve message exists, delete it
                                reserve_message = await interaction.channel.fetch_message(scrim['scrimConfiguration']['reserveMessage'])
                                await reserve_message.delete()

                                DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"scrimConfiguration.reserveMessage": None})
                                DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$pull": {"scrimConfiguration.registrationMessages": reserve_message.id}})

                        elif len(msgindex) >= scrim['scrimConfiguration']['maxTeams'] - 1: # If there are max_teams or more (-1 to remove unregistered team)
                            # Then swap first reserve index[max_teams + 1] with index[max_teams] (then delete unregistered team index)
                            # first_reserve refers to the team that was the first reserve | reserve_message refers to the message that was the reserve message
                            reserve_message = await interaction.channel.fetch_message(scrim['scrimConfiguration']['IDs']['reserveMessage']) # Reserve Message
                            first_reserve = await interaction.channel.fetch_message(msgindex[scrim['scrimConfiguration']['maxTeams']+ 1]) # First Reserve

                            reserve_message_raw = splitMessage(getMessages(interaction.guild.id)['scrimReserve'], interaction.guild.id, scrim["scrimName"])
                            reserve_message_embed = nextcord.Embed(title=reserve_message_raw[0], description=reserve_message_raw[1], color=White) # Build new reserve message

                            first_reserve_embed = nextcord.Embed(title=first_reserve.embeds[0].title, description=first_reserve.embeds[0].description)
                            if first_reserve.embeds[0].footer != None: first_reserve_embed.set_footer(text=first_reserve.embeds[0].footer.text) # Rebuild first reserve signup

                            DB.Scrimotron.SavedMessages.update_one({"messageID": reserve_message.id}, {"$set": {"messageID": first_reserve.id}}) # Update saved messages

                            new_view = AutomatedRegisterView(interaction=DB.Scrimotron.SavedMessages.find_one({"messageID": first_reserve.id})["interactionID"], type=None, guildID=interaction.guild.id, channelID=interaction.channel.id)

                            first_reserve_id = await reserve_message.edit(embed=first_reserve_embed, view=new_view) # Edit reserve message to first reserve
                            reserve_message_id = await first_reserve.edit(embed=reserve_message_embed, view=None) # Edit first reserve to reserve message

                            DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$set": {"scrimConfiguration.IDs.reserveMessage": reserve_message_id.id}})
                            DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$set": {f"scrimTeams.{first_reserve.embeds[0].title}.messageID": first_reserve_id.id}})

                        else: # Nothing happens (no reserves exist yet)
                            pass

                        DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$unset": {f"scrimTeams.{interaction.message.embeds[0].title}": ""}})
                        DB[str(interaction.guild.id)]["ScrimData"].update_one({"scrimName": scrim["scrimName"]}, {"$pull": {"scrimConfiguration.registrationMessages": team["messageID"]}})

                        message = await interaction.channel.fetch_message(team["messageID"])
                        await message.delete()
                        formatOutput(output=f"   {interaction.message.embeds[0].title} was unregistered!", status="Good", guildID=interaction.guild.id)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain and Admins can unregister teams!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "checkin":
                    if interaction.user.id == team["teamPlayer1"]:
                        if team["teamStatus"]["checkin"] == False:
                            DB[str(interaction.guild.id)]["TeamData"].update_one({"teamName": interaction.message.embeds[0].title}, {"$set": {"teamStatus.checkin": True}})
                            message = await interaction.channel.fetch_message(team["messageID"])
                            await message.edit(embed=message.embeds[0].set_footer(text="Checked In ✅"))

                            embed = nextcord.Embed(title="Team Checked In", description=f"**{interaction.message.embeds[0].title}** has been checked in for **{scrim["scrimName"]}**", color=Green)
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        else:
                            embed = nextcord.Embed(title="Team Already Checked In", description=f"**{interaction.message.embeds[0].title}** has already checked in!", color=Red)
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can check in!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "poi":
                    if interaction.user.id == team["teamPlayer1"]:
                        if scrim["scrimConfiguration"]["poiSelectionMode"] == "Simple": embed = nextcord.Embed(title=f"Select a POI for Map 1 ({scrim['scrimConfiguration']['maps']['map1']})", description="Selection Mode: Simple - Pick one POI per map\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI")
                        elif scrim["scrimConfiguration"]["poiSelectionMode"] == "Advanced": embed = nextcord.Embed(title=f"Select a POI for Map 1 ({scrim['scrimConfiguration']['maps']['map1']})", description="Selection Mode: Advanced - Option to pick Secondary POIs and Tridents\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI")

                        await interaction.response.send_message(embed=embed, view=POIView(interaction, scrim, team, map_num=1), ephemeral=True)

                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can open POI Selection!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback


class POIView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, scrim, team, map_num):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.scrim = scrim
        self.team = team

        for poi in MapData[f"{scrim['scrimConfiguration']['maps'][f'map{map_num}']}"]:
            if poi not in [team["teamPois"][f"map{map_num}"][f"map{map_num}POI"] for team in self.scrim["scrimTeams"].values()]: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.gray)
            else: button = nextcord.ui.Button(label=poi, style=nextcord.ButtonStyle.red, disabled=True)

            button.callback = self.create_callback(poi, map_num)
            self.add_item(button)

    def create_callback(self, poi, map_num):
        async def callback(interaction: nextcord.Interaction):
            try:
                DB[str(interaction.guild.id)]["TeamData"].update_one({"teamName": self.team["teamName"]}, {"$set": {f"teamPois.map{map_num}.map{map_num}POI": poi}})

                if self.scrim["scrimConfiguration"]["maps"]["map2"] != None:
                    if map_num == 2: # Edit message
                        message = DB[str(interaction.guild.id)]["TeamData"].find_one({"teamName": self.team["teamName"]})["messageID"]
                        channel = interaction.guild.get_channel(self.scrim["scrimConfiguration"]["registrationChannel"])

                        embed_title = message.embeds[0].title
                        embed_description = message.embeds[0].description

                        embed = nextcord.Embed(title=embed_title, description=f"POIs: {self.team['teamPois']['map1']['map1POI']} & {self.team['teamPois']['map2']['map2POI']}\n{embed_description}")
                        await interaction.message.edit(embed=embed)

                    else: # Open map 2 selection
                        embed = nextcord.Embed(f"Select a POI for Map 2 ({self.scrim['scrimConfiguration']['maps']['map2']})\nSelection Mode: Simple - Pick one POI per map\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that another team has picked that POI")
                        embed.set_footer(text=f"Map 1 Selection - {poi}")
                        await interaction.response.edit_message(embed=embed, view=POIView(interaction, self.scrim, self.team, map_num=2))

                else:
                    message = DB[str(interaction.guild.id)]["TeamData"].find_one({"teamName": self.team["teamName"]})["messageID"]
                    channel = interaction.guild.get_channel(self.scrim["scrimConfiguration"]["registrationChannel"])

                    embed_title = message.embeds[0].title
                    embed_description = message.embeds[0].description

                    embed = nextcord.Embed(title=embed_title, description=f"POI: {self.team['teamPois']['map1']['map1POI']}\n{embed_description}")
                    await interaction.message.edit(embed=embed)

                    embed = nextcord.Embed(title="POI Selection Confirmed", description=f"**{self.team['teamName']}** has selected **{poi}** for **{self.scrim['scrimName']}**", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class RegisterMenu(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, IDs, team_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.IDs = IDs
        self.team_data = team_data
        self.add_item(RegisterDropdown(interaction, IDs, self.team_data))

class RegisterDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, IDs, team_data):
        self.interaction = interaction
        self.IDs = IDs
        self.team_data = team_data
        super().__init__(placeholder="Select a scrim to sign up for", min_values=1, max_values=1, options=[nextcord.SelectOption(label=scrim['scrimName'], value=scrim['scrimName'], description=f"{scrim['scrimConfiguration']['teamType']} Scrim") for scrim in getScrims(command['guildID'])])

    async def callback(self, interaction: nextcord.Interaction):
        scrim = getScrim(command['guildID'], self.values[0])
        if scrim['scrimConfiguration']['teamType'] == 'Solos': # Correct Team Type
            if self.team_data[0] not in scrim['scrimTeams'].keys(): # Check if team name is already in scrim
                repeat = False
                for id in self.IDs[1:-2]: # Check if players are in other teams
                    if id == None: continue
                    if id in scrim['scrimConfiguration']['playerIDs']: repeat = True

                if repeat != True:
                    embed = nextcord.Embed(title=self.team_data[0], description=f"Player 1 - <@{self.IDs[1]}>")
                    embed.set_thumbnail(url=self.team_data[1])

                    message = await self.interaction.guild.get_channel(scrim["scrimConfiguration"]["registrationChannel"]).send(embed=embed, view=RegisterView(self.interaction))
                    DB.Scrimotron.SavedMessages.insert_one({"guildID": command['guildID'], "channelID": scrim["scrimConfiguration"]["registrationChannel"], "messageID": message.id, "interactionID": interaction.id, "viewType": "registration"})
                    DB[str(command['guildID'])]["ScrimData"].update_one({"scrimName": scrim['scrimName']}, {"$push": {"scrimConfiguration.registrationMessages": message.id}})
                    for id in self.IDs[1:-2]:
                        if id != None: DB[str(command['guildID'])]["ScrimData"].update_one({"scrimName": scrim['scrimName']}, {"$push": {"scrimConfiguration.playerIDs": id}})

                    DB[str(interaction.guild.id)]["ScrimData"].update_one(
                        {"scrimName": scrim['scrimName']},
                        {"$set": {f"scrimTeams.{self.team_data[0]}": {
                            "teamName": self.team_data[0],
                            "teamType": "Solos",
                            "teamLogo": self.team_data[1],
                            "teamPlayer1": self.IDs[1],
                            "teamPlayer2": self.IDs[2],
                            "teamPlayer3": self.IDs[3],
                            "teamSub1": self.IDs[4],
                            "teamSub2": self.IDs[5],
                            "teamPois": {
                                "map1": {
                                    "map1POI": None,
                                    "map1ID": None},
                                "map2": {
                                    "map2POI": None,
                                    "map2ID": None}},
                            "teamSetup": {
                                "roleID": None,
                                "channelID": None},
                            "teamStatus": {
                                "checkin": False,
                                "poiSelction": False},
                            "messageID": message.id
                            },
                        }})

                    if len(scrim["scrimTeams"]) + 1 == scrim["scrimConfiguration"]["maxTeams"]: # Final Team, send reserve message (+1 to include the new team)
                        message = splitMessage(getMessages(command['guildID'])['scrimReserve'], command["guildID"], self.values[0])

                        embed = nextcord.Embed(title=message[0], description=message[1], color=White)
                        message = await interaction.guild.get_channel(scrim["scrimConfiguration"]["registrationChannel"]).send(embed=embed)
                        DB[str(command['guildID'])]['ScrimData'].update_one({"scrimName": scrim['scrimName']}, {"$set": {"scrimConfiguration.IDs.reserveMessage": message.id}})
                        DB[str(command['guildID'])]['ScrimData'].update_one({"scrimName": scrim['scrimName']}, {"$push": {"scrimConfiguration.registrationMessages": message.id}})

                    embed = nextcord.Embed(title="Team Registered", description=f"**{self.team_data[0]}** has been registered for **{scrim['scrimName']}**", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)

                else: # A player appears in another team
                    embed = nextcord.Embed(title="Player Already in Team", description="One or more players are already in a team!", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

            else: # Team Name Already Exists
                embed = nextcord.Embed(title="Team Name Already Exists", description=f"Team name '{self.team_data[0]}' is already registered!\n*If you are trying to edit a team, you cannot edit solo registrations*\n*Instead unregister and register a new team*", color=Red)
                await interaction.response.edit_message(embed=embed, view=None)

        else:
            embed = nextcord.Embed(title="Invalid Team Type", description=f"This scrim is a {scrim['scrimConfiguration']['teamType']} sign up not Solos!", color=Red)
            await interaction.response.edit_message(embed=embed, view=None)

class Command_register_solo_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="register_solo", description="Register a solo team (Optional: Team Logo)")
    async def register_solo(self, interaction: nextcord.Interaction,
        team_name = nextcord.SlashOption(name="team_name", description="Enter a team name", required=True),
        player1: nextcord.User = nextcord.SlashOption(name="player_1", description="Enter player 1 (This will be the team captain)", required=True),
        team_logo = nextcord.SlashOption(name="team_logo", description="(Optional) Enter a team logo, (Submit a discord URL)", required=False)):

        global command
        command = {"name": interaction.application_command.name, "userID": interaction.user.id, "guildID": interaction.guild.id}
        formatOutput(output=f"/{command['name']} Used by {command['userID']} | @{interaction.user.name}", status="Normal", guildID=command["guildID"])

        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        try:
            scrims = getScrims(command['guildID'])

            if len(scrims) == 0: # No scrims found
                if interaction.user.guild_permissions.administrator == True: embed = nextcord.Embed(title="No Scrims Found", description="When your ready, Schedule scrims with `/schedule`!", color=Red)
                else: embed = nextcord.Embed(title="No Scrims Found", description="No scrims have been scheduled yet...\nWait for an admin to schedule a scrim!", color=Red)

                await interaction.edit_original_message(embed=embed)

            else: # More than 1 Scrim found, Convert users to IDs
                player1 = player1.id

                IDs = [None, player1, None, None, None, None, None, None]

                if player1 == interaction.user.id:
                    seen = set()
                    for id in IDs[1:-2]: # Check for duplicate players
                        if id == None: continue
                        if id in seen:
                            embed = nextcord.Embed(title="Duplicate Players", description="You cannot have duplicate players in a team!", color=Red)
                            await interaction.edit_original_message(embed=embed)
                            return
                        seen.add(id)

                        user = await bot.fetch_user(id)
                        if user == None: continue
                        if user.bot == False:

                            embed = nextcord.Embed(title=f"Registration Menu // {team_name}", description=f"**{team_name}**\nPlayer 1 - <@{player1}>", color=White)
                            embed.set_thumbnail(url=team_logo)

                            for scrim in getScrims(command['guildID']):
                                if scrim['scrimConfiguration']['teamType'] == 'Solos': team_type = '**Solos**'
                                else: team_type = scrim['scrimConfiguration']['teamType']

                                if scrim['scrimConfiguration']['maps']['map2'] != None: maps = f"Maps: {scrim['scrimConfiguration']['maps']['map1']} & {scrim['scrimConfiguration']['maps']['map2']}"
                                else: maps = f"Map: {scrim['scrimConfiguration']['maps']['map1']}"

                                embed.add_field(
                                    name=f"{scrim['scrimName']} - <t:{scrim['scrimEpoch']}:f> (<t:{scrim['scrimEpoch']}:R>)",
                                    value=f"Team Type: {team_type}\nPOI Selection Mode: {scrim['scrimConfiguration']['poiSelectionMode']}\n{maps}",
                                    inline=False
                                )

                            await interaction.edit_original_message(embed=embed, view=RegisterMenu(interaction, IDs, team_data=[team_name, team_logo]))

                        else: # Team contains bots
                            embed = nextcord.Embed(title="Invalid Player", description="You cannot have a bot in your team!", color=Red)
                            await interaction.edit_original_message(embed=embed)
                            break

                else: # Player 1 is not the user
                    embed = nextcord.Embed(title="Invaild Signup", description="When making a team you have to make yourself player 1 (Captain)", color=Red)
                    await interaction.edit_original_message(embed=embed)

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

def setup(bot):
    bot.add_cog(Command_register_solo_Cog(bot))