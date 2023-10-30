import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, channel_registration, errorResponse
from Config import db_team_data

class Command_register_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="register", description="Register a team")
    async def register(self, interaction: nextcord.Interaction, team_name: str, captain: nextcord.User, player2: nextcord.User , player3: nextcord.User, sub1: nextcord.User = None, sub2: nextcord.User = None, logo: str = None):
        command = 'register'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.response.defer(ephemeral=True)
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
                "team_number" : db_team_data.count_documents({}) + 1,
                "captain": captain.id,
                "player2": player2.id,
                "player3": player3.id,
                "sub1": sub1,
                "sub2": sub2,
                "logo": logo,
                "setup": {
                    "roleID": "None",
                    "channelID": "None"
                }
            })

            if logo != "None": embed.set_thumbnail(url=logo)
            await interaction.edit_original_message(content=f"{team_name} has been registered!")
            embed.set_footer(text=f"Team {db_team_data.count_documents({})} | Registered at {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC")
            await self.bot.get_channel(channel_registration).send(embed=embed)
            formatOutput(output=f"   {team_name} was registered!", status="Good")

        except Exception as e:
            try: db_team_data.find_one_and_delete({"team_name": team_name}) # delete team if it was created but an error occured
            except: pass # if team wasnt created yet, ignore
            await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_register_Cog(bot))