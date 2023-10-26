import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, channel_registration
from Config import db_team_data

class Command_unregister_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="unregister", description="Unregister a team")
    async def unregister(self, interaction: nextcord.Interaction, team_name: str):
        command = 'unregister'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.response.defer(ephemeral=True)
        if db_team_data.find_one({"team_name": team_name}) != None: # team exists
            data = db_team_data.find_one({"team_name": team_name})
            if interaction.user.id == data["captain"]: # user is captain
                db_team_data.delete_one({"team_name": team_name}) # delete team from DB
                messages = await interaction.channel.history(limit=20).flatten() # delete team from channel
                for msg in messages:
                    if msg.author.bot:
                        embed = msg.embeds[0]
                        if embed.title == team_name:
                            await msg.delete()
                            break
                await interaction.edit_original_message(content=f"{team_name} has been unregistered!")
            else: 
                await interaction.edit_original_message(content=f"You are not the captain of {team_name}!")
        else:
            await interaction.edit_original_message(content=f"Team {team_name} not found!")

def setup(bot):
    bot.add_cog(Command_unregister_Cog(bot))