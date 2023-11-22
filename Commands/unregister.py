import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, channel_registration, errorResponse, partipantRoleID
from Config import db_team_data

class Command_unregister_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="unregister", description="Unregister a team")
    async def unregister(self, interaction: nextcord.Interaction, team_name: str):
        command = 'unregister'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer(ephemeral=True)

        try:
            if db_team_data.find_one({"team_name": team_name}) != None: # team exists
                data = db_team_data.find_one({"team_name": team_name})
                if interaction.user.id == data["captain"]: # user is captain
                    db_team_data.delete_one({"team_name": team_name}) # delete team from DB
                    channel = interaction.guild.get_channel(channel_registration) # delete team from registration channel
                    messages = await channel.history(limit=20).flatten()
                    for msg in messages:
                        if msg.author.bot:
                            embed = msg.embeds[0]
                            if embed.title == team_name:
                                await msg.delete()
                                role = interaction.guild.get_role(partipantRoleID)
                                await interaction.guild.get_member(data["captain"]).remove_roles(role)
                                await interaction.guild.get_member(data["player2"]).remove_roles(role)
                                await interaction.guild.get_member(data["player3"]).remove_roles(role)
                                if data["sub1"] != "N/A": await interaction.guild.get_member(data["sub1"]).remove_roles(role)
                                if data["sub2"] != "N/A": await interaction.guild.get_member(data["sub2"]).remove_roles(role)
                                break
                    await interaction.edit_original_message(content=f"{team_name} has been unregistered!")
                    formatOutput(output=f"   /{command} was successful!", status="Good")
                else:
                    if interaction.user.guild_permissions.administrator: # not captain, but is admin
                        db_team_data.delete_one({"team_name": team_name})
                        channel = interaction.guild.get_channel(channel_registration) # delete team from registration channel
                        messages = await channel.history(limit=20).flatten()
                        for msg in messages:
                            if msg.author.bot:
                                embed = msg.embeds[0]
                                if embed.title == team_name:
                                    await msg.delete()
                                    role = interaction.guild.get_role(partipantRoleID)
                                    await interaction.guild.get_member(data["captain"]).remove_roles(role)
                                    await interaction.guild.get_member(data["player2"]).remove_roles(role)
                                    await interaction.guild.get_member(data["player3"]).remove_roles(role)
                                    if data["sub1"] != "N/A": await interaction.guild.get_member(data["sub1"]).remove_roles(role)
                                    if data["sub2"] != "N/A": await interaction.guild.get_member(data["sub2"]).remove_roles(role)
                                    break
                        await interaction.edit_original_message(content=f"{team_name} has been unregistered!")
                        formatOutput(output=f"   /{command} | {team_name} was unregistered", status="Good")
                    else: # not admin
                        await interaction.edit_original_message(content=f"You are not the captain of {team_name}!")
                        formatOutput(output=f"   /{command} | {userID} is not captain of {team_name}!", status="Warning")
            else:
                await interaction.edit_original_message(content=f"Team {team_name} not found!")
                formatOutput(output=f"   /{command} | {team_name} not found!", status="Warning")

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_unregister_Cog(bot))