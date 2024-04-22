import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, DB, getTeams, getChannels

class Command_unregister_all_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="unregister_all", description="Unregisters all players/teams. **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def unregister_all(self, interaction: nextcord.Interaction):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        try:
            channel = getChannels(guildID)["scrimRegistrationChannel"]
            for team in getTeams(guildID): 
                message = await interaction.guild.get_channel(channel).fetch_message(team["teamSetup"]["messageID"])
                await message.delete()

            # for i in data:
            #     role = interaction.guild.get_role(partipantRoleID)
            #     await interaction.guild.get_member(i["captain"]).remove_roles(role)
            #     await interaction.guild.get_member(i["player2"]).remove_roles(role)
            #     await interaction.guild.get_member(i["player3"]).remove_roles(role)
            #     if i["sub1"] != "N/A": await interaction.guild.get_member(i["sub1"]).remove_roles(role)
            #     if i["sub2"] != "N/A": await interaction.guild.get_member(i["sub2"]).remove_roles(role)
                DB[str(interaction.guild.id)]["TeamData"].delete_many({})
                formatOutput(output=f"   /{command} | {team['teamName']} was unregistered", status="Good", guildID=guildID)

            await interaction.edit_original_message(content=f"All Teams have been unregistered!")
            formatOutput(output=f"   /{command} was successful!", status="Good", guildID=guildID)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_unregister_all_Cog(bot))