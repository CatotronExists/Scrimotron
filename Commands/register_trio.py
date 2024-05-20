import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, DB, getTeams, getChannels, getScrims, getScrim, getTeam, getMessages, splitMessage
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
            team = DB[str(interaction.guild.id)]["ScrimData"].find_one({"teamName": interaction.message.embeds[0].title})
            print(team)
            try:
                if custom_id == "edit":
                    if interaction.user.id == team["teamPlayer1"]:
                        embed = nextcord.Embed(title="Run `/register` to edit your signup!", color=White)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain can edit signups!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "unregister":
                    if interaction.user.id == team["teamPlayer1"] or interaction.user.guild_permissions.administrator == True:
                        message = await interaction.channel.fetch_message(team["teamSetup"]["messageID"])
                        await message.delete()
                        DB[str(interaction.guild.id)]["TeamData"].delete_one({"teamName": interaction.message.embeds[0].title})
                        formatOutput(output=f"   {interaction.message.embeds[0].title} was unregistered!", status="Good", guildID=interaction.guild.id)
                    else:
                        embed = nextcord.Embed(title="Only the Team Captain and Staff can unregister teams!", color=Red)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())
        return callback

class CheckinView(nextcord.ui.View):
    pass

class RegisterMenu(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, IDs, team_data):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.IDs = IDs
        self.team_data = team_data
        self.add_item(RegisterDropdown(interaction, self.IDs, self.team_data))

class RegisterDropdown(nextcord.ui.Select):
    def __init__(self, interaction: nextcord.Interaction, IDs, team_data):
        self.interaction = interaction
        self.IDs = IDs
        self.team_data = team_data
        super().__init__(placeholder="Select a scrim to sign up for", min_values=1, max_values=1, options=[nextcord.SelectOption(label=scrim['scrimName'], value=scrim['scrimName'], description=f"{scrim['scrimConfiguration']['teamType']} Scrim") for scrim in getScrims(command['guildID'])])

    async def callback(self, interaction: nextcord.Interaction):
        scrim = getScrim(command['guildID'], self.values[0])
        if scrim['scrimConfiguration']['teamType'] == 'Trios': # Correct Team Type
            if self.team_data[0] not in scrim['scrimTeams'].keys(): # Check if team name is already in scrim
                if len(scrim["scrimTeams"]) + 1 <= scrim["scrimConfiguration"]["maxTeams"]: # Check if team needs to be in reserve
                    embed = nextcord.Embed(title="Team Registered", description=f"**{self.team_data[0]}** has been registered for **{scrim['scrimName']}**", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)

                    embed = nextcord.Embed(title=self.team_data[0], description=f"Player 1 - <@{self.IDs[1]}>\nPlayer 2 - <@{self.IDs[2]}>\nPlayer 3 - <@{self.IDs[3]}>\nSub 1 - {self.IDs[6]}\nSub 2 - {self.IDs[7]}")
                    embed.set_thumbnail(url=self.team_data[1])

                    message = await self.interaction.guild.get_channel(scrim["scrimConfiguration"]["registrationChannel"]).send(embed=embed, view=RegisterView(self.interaction))
                    DB.Scrimotron.SavedMessages.insert_one({"guildID": command['guildID'], "channelID": scrim["scrimConfiguration"]["registrationChannel"], "messageID": message.id, "interactionID": interaction.id, "viewType": "registration"})

                    DB[str(interaction.guild.id)]["ScrimData"].update_one(
                        {"scrimName": scrim['scrimName']},
                        {"$set": {f"scrimTeams.{self.team_data[0]}": {
                            "teamType": "Trios",
                            "teamLogo": self.team_data[1],
                            "teamPlayer1": self.IDs[1],
                            "teamPlayer2": self.IDs[2],
                            "teamPlayer3": self.IDs[3],
                            "teamSub1": self.IDs[4],
                            "teamSub2": self.IDs[5],
                            "teamPois": {
                                "map1": {
                                    "map1POI": None,
                                    "map1Secondary": None,
                                    "map1Split": None,
                                    "map1Vechicle": None},
                                "map2": {
                                    "map2POI": None,
                                    "map2Secondary": None,
                                    "map2Split": None,
                                    "map2Vechicle": None}},
                            "teamSetup": {
                                "checkinMessageID": None,
                                "poiMessageID": None,
                                "roleID": None,
                                "channelID": None},
                            "teamStatus": {
                                "checkin": False,
                                "poiSelction": False},
                            "messageID": message.id
                            },
                        }})
                    
                    if len(scrim["scrimTeams"]) + 1 == scrim["scrimConfiguration"]["maxTeams"]: # Final Team, send reserve message
                        message = splitMessage(getMessages(command['guildID'])['scrimReserve'], interaction.guild.id)
                        message_split = message.split("\n")
                        title = message_split[0]
                        description = '\n'.join(message_split[1:])

                        embed = nextcord.Embed(title=title, description=description, color=White)
                        message = await interaction.guild.get_channel(scrim["scrimConfiguration"]["registrationChannel"]).send(embed=embed)
                        DB[command['guildID']]['ScrimData'].update_one({"scrimName": scrim['scrimName']}, {"$set": {"scrimConfiguration.IDs.reserveMessage": message.id}})

            else: # Team Name Already Exists
                team = getTeam(command['guildID'], self.values[0], self.team_data[0])
                if team['teamPlayer1'] == self.IDs[1]: # Check if team captain is the same, if so, edit registration
                    message = await self.interaction.guild.get_channel(scrim["scrimConfiguration"]["registrationChannel"]).fetch_message(team['messageID'])

                    embed = nextcord.Embed(title=self.team_data[0], description=f"Player 1 - <@{self.IDs[1]}>\nPlayer 2 - <@{self.IDs[2]}>\nPlayer 3 - <@{self.IDs[3]}>\nSub 1 - {self.IDs[6]}\nSub 2 - {self.IDs[7]}")
                    embed.set_thumbnail(url=self.team_data[1])

                    await message.edit(embed=embed, view=RegisterView(self.interaction))

                else: 
                    embed = nextcord.Embed(title="Team Name Already Exists", description=f"Team name '{self.team_data[0]}' is already registered!", color=Red)
                    await interaction.response.edit_message(embed=embed, view=None)

        else:
            embed = nextcord.Embed(title="Invalid Team Type", description=f"This scrim is a {scrim['scrimConfiguration']['teamType']} sign up not Trios!", color=Red)
            await interaction.response.edit_message(embed=embed, view=None)

class Command_register_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="register_trio", description="Register a trio team (Optional: Upto Two Subs + Team Logo)")
    async def register(self, interaction: nextcord.Interaction,
        team_name = nextcord.SlashOption(name="team_name", description="Enter a team name", required=True),
        player1: nextcord.User = nextcord.SlashOption(name="player_1", description="Enter player 1 (This will be the team captain)", required=True),
        player2: nextcord.User = nextcord.SlashOption(name="player_2", description="Enter player 2", required=True),
        player3: nextcord.User = nextcord.SlashOption(name="player_3", description="Enter player 3", required=True),
        sub1: nextcord.User = nextcord.SlashOption(name="sub_1", description="(Optional) Enter sub 1", required=False),
        sub2: nextcord.User = nextcord.SlashOption(name="sub_2", description="(Optional) Enter sub 2", required=False),
        team_logo = nextcord.SlashOption(name="team_logo", description="(Optional) Enter a team logo, (Submit a discord URL)", required=False)):

        global command
        command = {"name": interaction.application_command.name, "userID": interaction.user.id, "guildID": interaction.guild.id}
        formatOutput(output=f"/{command['name']} Used by {command['userID']} | @{interaction.user.name}", status="Normal", guildID=command["guildID"])

        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        try: 
            scrims = getScrims(command['guildID'])

            if len(scrims) == 0: # No scrims found
                if interaction.user.guild_permissions.administrator == True:
                    embed = nextcord.Embed(title="No Scrims Found", description="When your ready, Schedule scrims with `/schedule`!", color=Red)
                    await interaction.edit_original_message(embed=embed)
                    return

                else:
                    embed = nextcord.Embed(title="No Scrims Found", description="No scrims have been scheduled yet...\nWait for an admin to schedule a scrim!", color=Red)
                    await interaction.edit_original_message(embed=embed)
                    return

            else: # More than 1 Scrim found

                # Convert users to IDs
                player1 = player1.id
                player2 = player2.id
                player3 = player3.id

                if sub1 != None:
                    sub1 = sub1.id
                    sub1_display = f"<@{sub1}>"
                else: sub1_display = "**None**"
                if sub2 != None:
                    sub2 = sub2.id
                    sub2_display = f"<@{sub2}>"
                else: sub2_display = "**None**"

                IDs = [None, player1, player2, player3, sub1, sub2, sub1_display, sub2_display]

                embed = nextcord.Embed(title=f"Registration Menu // {team_name}", description=f"**{team_name}**\nPlayer 1 - <@{player1}>\nPlayer 2 - <@{player2}>\nPlayer 3 - <@{player3}>\nSub 1 - {sub1_display}\nSub 2 - {sub2_display}", color=White)
                embed.set_thumbnail(url=team_logo)

                for scrim in getScrims(command['guildID']):
                    if scrim['scrimConfiguration']['teamType'] == 'Trios': team_type = '**Trios**'
                    else: team_type = scrim['scrimConfiguration']['teamType']

                    if scrim['scrimConfiguration']['maps']['map2'] != None: maps = f"Maps: {scrim['scrimConfiguration']['maps']['map1']} & {scrim['scrimConfiguration']['maps']['map2']}"
                    else: maps = f"Map: {scrim['scrimConfiguration']['maps']['map1']}"

                    embed.add_field(
                        name=f"{scrim['scrimName']} - <t:{scrim['scrimEpoch']}:f> (<t:{scrim['scrimEpoch']}:R>)",
                        value=f"Team Type: {team_type}\nPOI Selection Mode: {scrim['scrimConfiguration']['poiSelectionMode']}\n{maps}",
                        inline=False
                    )

            await interaction.edit_original_message(embed=embed, view=RegisterMenu(interaction, IDs, team_data=[team_name, team_logo]))

        except Exception as e: await errorResponse(e, command, interaction, error_traceback=traceback.format_exc())

def setup(bot):
    bot.add_cog(Command_register_Cog(bot))