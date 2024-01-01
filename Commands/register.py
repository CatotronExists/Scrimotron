import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, channel_registration, errorResponse, partipantRoleID
from Config import db_team_data

class Command_register_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="register", description="Register a team")
    async def register(self, interaction: nextcord.Interaction, team_name: str, captain: nextcord.User, player2: nextcord.User , player3: nextcord.User, sub1: nextcord.User = None, sub2: nextcord.User = None, logo: str = None):
        command = 'register'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer(ephemeral=True)

        data = list(db_team_data.find())
        already_registered = False
        for i in data:
            if i["team_name"] == team_name:
                await interaction.edit_original_message(content=f"Team name '{team_name}' is already registered!")
                formatOutput(output=f"   /{command} | team name '{team_name}' is already registered!", status="Error")
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

                db_team_data.insert_one({
                    "team_name": team_name,
                    "captain": captain.id,
                    "player2": player2.id,
                    "player3": player3.id,
                    "sub1": sub1,
                    "sub2": sub2,
                    "logo": logo,
                    "pois": {
                        "map1": "None",
                        "map1_secondary": "None",
                        "map1_split": "None",
                        "map1_vechicle": "None",
                        "map2": "None",
                        "map2_secondary": "None",
                        "map2_split": "None",
                        "map2_vechicle": "None"
                        
                    },
                    "setup": {
                        "roleID": "None",
                        "channelID": "None",
                        "check_in": "no"
                    }
                })

                if logo != "None": embed.set_thumbnail(url=logo)

                role = interaction.guild.get_role(partipantRoleID)
                await interaction.guild.get_member(captain.id).add_roles(role)
                await interaction.guild.get_member(player2.id).add_roles(role)
                await interaction.guild.get_member(player3.id).add_roles(role)
                if sub1 != "N/A": await interaction.guild.get_member(sub1).add_roles(role)
                if sub2 != "N/A": await interaction.guild.get_member(sub2).add_roles(role)

                await interaction.edit_original_message(content=f"{team_name} has been registered!")
                embed.set_footer(text=f"Registered at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC")
                await self.bot.get_channel(channel_registration).send(embed=embed)
                formatOutput(output=f"   {team_name} was registered!", status="Good")
                formatOutput(output=f"   /{command} was successful!", status="Good")

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
                try: 
                    db_team_data.find_one_and_delete({"team_name": team_name}) # delete team if it was created but an error occured
                    formatOutput(output=f"   /{command} | saved team was deleted, due to error", status="Error")
                except: pass # if team wasnt created yet, ignore

def setup(bot):
    bot.add_cog(Command_register_Cog(bot))