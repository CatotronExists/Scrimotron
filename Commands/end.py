import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID
from Config import db_team_data, db_bot_data

class Command_end_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="end", description="End United", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def end(self, interaction: nextcord.Interaction):
        command = 'end'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.response.defer(ephemeral=True)
        try:
            catergory_vc = db_bot_data.find_one({"vc_catergory": {"$exists": True}})["vc_catergory"]
            data = list(db_team_data.find())
            for i in data:
                await interaction.guild.get_role(i["setup"]["roleID"]).delete()
                await interaction.guild.get_channel(i["setup"]["channelID"]).delete()
                db_team_data.update_one(
                    {"team_name": i["team_name"]}, 
                    {"$set": {"setup.roleID": "None", "setup.channelID": "None"}})
            await interaction.guild.get_role(db_bot_data.find_one({"participant_role": {"$exists": True}})["participant_role"]).delete()
            await interaction.guild.get_channel(catergory_vc).delete()
            await interaction.edit_original_message(content=f"UnitedOCE has ended!")

            db_bot_data.delete_one({"vc_catergory": catergory_vc})
        except Exception as e:
            await interaction.edit_original_message(content=f"Something went wrong while ending UnitedOCE. Error: {e}")

def setup(bot):
    bot.add_cog(Command_end_Cog(bot))