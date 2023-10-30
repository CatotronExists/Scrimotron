import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_registration
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
        started_at = datetime.datetime.utcnow()
        try:
            data = list(db_team_data.find())
            embed = nextcord.Embed(title="Ending UnitedOCE", color=0x000)
            embed.add_field(name="Deleting Roles", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting VCs", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting Team Data", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting Registrations", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting Participant Role", value=f"0/1", inline=True)
            embed.add_field(name="Deleting VC Catergory", value=f"0/1", inline=True)
            await interaction.edit_original_message(embed=embed)

            teams_processed = 0
            error = False
            try: # delete roles and channels
                for i in data:
                    await interaction.guild.get_role(i["setup"]["roleID"]).delete()
                    await interaction.guild.get_channel(i["setup"]["channelID"]).delete()
                    db_team_data.delete_one({"team_name": i["team_name"]})
                    teams_processed += 1
                    embed.set_field_at(0, name="Deleting Roles", value=f"{teams_processed}/{len(data)}", inline=True)
                    embed.set_field_at(1, name="Deleting VCs", value=f"{teams_processed}/{len(data)}", inline=True)
                    embed.set_field_at(2, name="Deleting Team Data", value=f"{teams_processed}/{len(data)}", inline=True)
                    await interaction.edit_original_message(embed=embed)
                embed.set_field_at(0, name="Deleting Roles", value=f"**DONE**", inline=True)
                embed.set_field_at(1, name="Deleting VCs", value=f"**DONE**", inline=True)
                embed.set_field_at(2, name="Deleting Team Data", value=f"**DONE**", inline=True)
            except Exception as e:
                embed.set_field_at(0, name="Deleting Roles", value=f"**FAILED**", inline=True)
                embed.set_field_at(1, name="Deleting VCs", value=f"**FAILED**", inline=True)
                embed.set_field_at(2, name="Deleting Team Data", value=f"**FAILED**", inline=True)
                await errorResponse(error=e, command=command, interaction=interaction)
                error = True
            
            try: # delete registrations
                channel = interaction.guild.get_channel(channel_registration)
                messages = await channel.history(limit=100).flatten()
                for msg in messages:
                    if msg.author.bot:
                        await msg.delete()
                embed.set_field_at(3, name="Deleting Registrations", value=f"**DONE**", inline=True)
            except Exception as e:
                embed.set_field_at(3, name="Deleting Registrations", value=f"**FAILED**", inline=True)
                await errorResponse(error=e, command=command, interaction=interaction)
                error = True

            try: # delete participant role
                await interaction.guild.get_role(db_bot_data.find_one({"participant_role": {"$exists": True}})["participant_role"]).delete()
                db_bot_data.delete_one({"participant_role": {"$exists": True}})
                embed.set_field_at(4, name="Deleting Participant Role", value=f"**DONE**", inline=True)
            except Exception as e:
                embed.set_field_at(4, name="Deleting Participant Role", value=f"**FAILED**", inline=True)
                await errorResponse(error=e, command=command, interaction=interaction)
                error = True

            try: # delete vc catergory
                catergory_vc = db_bot_data.find_one({"vc_catergory": {"$exists": True}})["vc_catergory"]
                await interaction.guild.get_channel(catergory_vc).delete()
                db_bot_data.delete_one({"vc_catergory": catergory_vc})
                embed.set_field_at(5, name="Deleting VC Catergory", value=f"**DONE**", inline=True)
            except Exception as e:
                embed.set_field_at(5, name="Deleting VC Catergory", value=f"**FAILED**", inline=True)
                await errorResponse(error=e, command=command, interaction=interaction)
                error = True

            if error == False:
                time_taken = datetime.datetime.strftime(datetime.datetime(1, 1, 1) + (datetime.datetime.utcnow() - started_at), "%M:%S")
                embed.set_footer(text=f"Took {time_taken} to complete")
                embed.title = "UnitedOCE has ended!"
                await interaction.edit_original_message(embed=embed)

        except Exception as e:
            await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_end_Cog(bot))