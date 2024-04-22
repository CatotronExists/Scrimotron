import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, DB, getTeams, getChannels

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
            team = DB[str(interaction.guild.id)]["TeamData"].find_one({"teamName": interaction.message.embeds[0].title})
            try:
                if custom_id == "edit":
                    if interaction.user.id == team["teamCaptain"]:
                        embed = nextcord.Embed(title="Run `/register` to edit your signup!", color=0x008000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else: 
                        embed = nextcord.Embed(title="Only the Team Captain can edit signups!", color=0xFF0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                elif custom_id == "unregister":
                    if interaction.user.id == team["teamCaptain"] or interaction.user.guild_permissions.administrator == True:
                        message = await interaction.channel.fetch_message(team["teamSetup"]["messageID"])
                        await message.delete()
                        DB[str(interaction.guild.id)]["TeamData"].delete_one({"teamName": interaction.message.embeds[0].title})
                        formatOutput(output=f"   {interaction.message.embeds[0].title} was unregistered!", status="Good", guildID=interaction.guild.id)
                    else: 
                        embed = nextcord.Embed(title="Only the Team Captain and Staff can unregister teams!", color=0xFF0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)
        return callback

class Command_register_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="register", description="Register a team")
    async def register(self, interaction: nextcord.Interaction, team_name: str, captain: nextcord.User, player2: nextcord.User , player3: nextcord.User, sub1: nextcord.User = None, sub2: nextcord.User = None, logo: str = None):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)
        
        try: await interaction.response.defer(ephemeral=True)
        except: pass

        team_data = getTeams(interaction.guild.id)
        already_registered = False
        for team in team_data:
            if team["teamName"] == team_name:
                await interaction.edit_original_message(content=f"Team name '{team_name}' is already registered!")
                formatOutput(output=f"   /{command} | Team name '{team_name}' is already registered!", status="Error", guildID=guildID)
                already_registered = True
                break

        if already_registered == False:
            if logo == None: logo = "None"
            try:
                if sub1 == None and sub2 == None: # no subs
                    sub1 = sub2 = "N/A"
                    embed = nextcord.Embed(title=team_name, description=f"**Captain:** {captain.mention}\n**Player 2:** {player2.mention}\n**Player 3:** {player3.mention}\n**Sub 1:** {sub1}\n**Sub 2:** {sub2}", color=0x000)

                elif sub2 == None: # only 1 sub
                    sub2 = "N/A"
                    embed = nextcord.Embed(title=team_name, description=f"**Captain:** {captain.mention}\n**Player 2:** {player2.mention}\n**Player 3:** {player3.mention}\n**Sub 1:** {sub1.mention}\n**Sub 2:** {sub2}", color=0x000)
                    sub1 = sub1.id

                else: # two subs
                    embed = nextcord.Embed(title=team_name, description=f"**Captain:** {captain.mention}\n**Player 2:** {player2.mention}\n**Player 3:** {player3.mention}\n**Sub 1:** {sub1.mention}\n**Sub 2:** {sub2.mention}", color=0x000)
                    sub1 = sub1.id
                    sub2 = sub2.id

                DB[guildID]["TeamData"].insert_one({
                    "teamName": team_name, 
                    "teamCaptain": captain.id, 
                    "teamPlayer2": player2.id, 
                    "teamPlayer3": player3.id, 
                    "teamSub1": sub1, 
                    "teamSub2": sub2, 
                    "teamLogo": logo,
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
                        "roleID": None,
                        "channelID": None,
                        "messageID": None},
                    "teamStatus": {
                        "checkin": False,
                        "poiSelction": False}
                    })

                if logo != "None": embed.set_thumbnail(url=logo)

                # role = interaction.guild.get_role(partipantRoleID)
                # await interaction.guild.get_member(captain.id).add_roles(role)
                # await interaction.guild.get_member(player2.id).add_roles(role)
                # await interaction.guild.get_member(player3.id).add_roles(role)
                # if sub1 != "N/A": await interaction.guild.get_member(sub1).add_roles(role)
                # if sub2 != "N/A": await interaction.guild.get_member(sub2).add_roles(role)

                embed.set_footer(text=f"Registered at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC")
                
                channels = getChannels(interaction.guild.id)
                message = await self.bot.get_channel(channels["scrimRegistrationChannel"]).send(embed=embed, view=RegisterView(interaction))

                DB[str(interaction.guild.id)]["TeamData"].update_one({"teamName": team_name}, {"$set": {"teamSetup": {"roleID": None, "channelID": None, "messageID": message.id}}}, upsert=True)
                DB.Scrimotron.GlobalData.find_one_and_update({"savedMessages": {"$exists": True}}, {"$push": {"savedMessages": {"guildID": interaction.guild.id, "channelID": channels["scrimRegistrationChannel"], "messageID": message.id, "interactionID": interaction.id, "viewType": "registration"}}}, upsert=True)

                await interaction.edit_original_message(content=f"{team_name} has been registered!")
                formatOutput(output=f"   {team_name} was registered!", status="Good", guildID=guildID)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
                try: 
                    DB[str(interaction.guild.id)]["TeamData"].delete_one({"teamName": team_name}) # delete team if it was created but an error occured
                    formatOutput(output=f"   /{command} | Team creation was cancelled, due to error", status="Error", guildID=guildID)
                except: pass # if team wasnt created yet, ignore

def setup(bot):
    bot.add_cog(Command_register_Cog(bot))