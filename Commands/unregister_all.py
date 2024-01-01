import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, channel_registration, errorResponse, partipantRoleID
from Config import db_team_data

class Command_unregister_all_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="unregister_all", description="unregister all teams", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def unregister_all(self, interaction: nextcord.Interaction):
        command = 'unregister_all'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer(ephemeral=True)

        try:
            channel = interaction.guild.get_channel(channel_registration) # delete team from registration channel
            messages = await channel.history(limit=20).flatten()
            for msg in messages:
                await msg.delete()

            data = list(db_team_data.find())
            for i in data:
                role = interaction.guild.get_role(partipantRoleID)
                await interaction.guild.get_member(i["captain"]).remove_roles(role)
                await interaction.guild.get_member(i["player2"]).remove_roles(role)
                await interaction.guild.get_member(i["player3"]).remove_roles(role)
                if i["sub1"] != "N/A": await interaction.guild.get_member(i["sub1"]).remove_roles(role)
                if i["sub2"] != "N/A": await interaction.guild.get_member(i["sub2"]).remove_roles(role)
                db_team_data.delete_one({"team_name": i["team_name"]})
                formatOutput(output=f"   /{command} | {i['team_name']} was unregistered", status="Good")

                await interaction.edit_original_message(content=f"All Teams have been unregistered!")
                formatOutput(output=f"   /{command} was successful!", status="Good")

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_unregister_all_Cog(bot))