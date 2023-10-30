import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, channel_checkin, errorResponse
from Config import db_team_data

class Command_check_in_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="check_in", description="Open check ins", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def check_in(self, interaction: nextcord.Interaction):
        command = 'check_in'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.response.defer(ephemeral=True)

        await interaction.edit_original_message(content="Check ins are opening...")
        try:
            data = list(db_team_data.find())
            for i in data:
                await interaction.guild.get_channel(channel_checkin).send(content=f"**Team {i['team_number']}**\n{i['team_name']}\n*Captain:* <@{i['captain']}>")
            await interaction.edit_original_message(content="Check ins have opened!")

        except Exception as e:
            errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_check_in_Cog(bot))