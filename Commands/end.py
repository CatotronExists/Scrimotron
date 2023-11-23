import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, partipantRoleID, channel_poi, channel_checkin, channel_bot_event
from Config import db_team_data, db_bot_data

class Command_end_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="end", description="End United", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def end(self, interaction: nextcord.Interaction):
        command = 'end'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        await interaction.response.defer(ephemeral=True)
        started_at = datetime.datetime.utcnow()
        try:
            data = list(db_team_data.find())
            embed = nextcord.Embed(title="Ending UnitedOCE", color=0x000)
            embed.add_field(name="Deleting Roles", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting VCs", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting Team Data", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Deleting POIs & Checkins", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Changing Permissions", value=f"0/1", inline=True)
            embed.add_field(name="Deleting VC Catergory", value=f"0/1", inline=True)
            await interaction.edit_original_message(embed=embed)

            teams_processed = 0
            error = False
            try: # delete roles and channels
                for i in data:
                    try: await interaction.guild.get_role(i["setup"]["roleID"]).delete()
                    except: pass
                    try: await interaction.guild.get_channel(i["setup"]["channelID"]).delete()
                    except: pass
                    db_team_data.update_one({
                        "team_name": i["team_name"]}
                        , {
                        "$set": {
                        "pois.map1": "None",
                        "pois.map2": "None",
                        "setup.roleID": "None",
                        "setup.channelID": "None"
                        }})
                    teams_processed += 1
                    embed.set_field_at(0, name="Deleting Roles", value=f"{teams_processed}/{len(data)}", inline=True)
                    embed.set_field_at(1, name="Deleting VCs", value=f"{teams_processed}/{len(data)}", inline=True)
                    embed.set_field_at(2, name="Deleting Team Data", value=f"{teams_processed}/{len(data)}", inline=True)
                    await interaction.edit_original_message(embed=embed)
                embed.set_field_at(0, name="Deleting Roles", value=f"**DONE**", inline=True)
                embed.set_field_at(1, name="Deleting VCs", value=f"**DONE**", inline=True)
                embed.set_field_at(2, name="Deleting Team Data", value=f"**DONE**", inline=True)
                await interaction.edit_original_message(embed=embed)
            except Exception as e:
                embed.set_field_at(0, name="Deleting Roles", value=f"**FAILED**", inline=True)
                embed.set_field_at(1, name="Deleting VCs", value=f"**FAILED**", inline=True)
                embed.set_field_at(2, name="Deleting Team Data", value=f"**FAILED**", inline=True)
                error_traceback = traceback.format_exc()
                await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
                error = True

            try: # delete POIs & Checkins
                channel = interaction.guild.get_channel(channel_poi) # delete POIs
                messages = await channel.history(limit=25).flatten()
                for msg in messages:
                    if msg.author.bot:
                        await msg.delete()
                db_bot_data.delete_one({"maps": {"$exists": True}}) # remove from db

                channel = interaction.guild.get_channel(channel_checkin) # delete checkins
                messages = await channel.history(limit=25).flatten()
                messages_deleted = 0
                for msg in messages:
                    if msg.author.bot:
                        await msg.delete()
                        messages_deleted += 1
                        embed.set_field_at(3, name="Deleting POIs & Checkins", value=f"{messages_deleted}/{len(data)}", inline=True)
                        await interaction.edit_original_message(embed=embed)

                embed.set_field_at(3, name="Deleting POIs & Checkins", value=f"**DONE**", inline=True)
                await interaction.edit_original_message(embed=embed)
            except Exception as e:
                embed.set_field_at(3, name="Deleting POIs & Checkins", value=f"**FAILED**", inline=True)
                error_traceback = traceback.format_exc()
                await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
                error = True

            try: # Changing Permissions
                role = interaction.guild.get_role(partipantRoleID)
                members = interaction.guild.members
                players_processed = 0
                for member in members:
                    await member.remove_roles(role)
                    players_processed += 1
                    embed.set_field_at(4, name="Changing Permissions", value=f"{players_processed}/{len(members)}", inline=True)
                embed.set_field_at(4, name="Changing Permissions", value=f"**DONE**", inline=True)
            except Exception as e:
                embed.set_field_at(4, name="Changing Permissions", value=f"**FAILED**", inline=True)
                error_traceback = traceback.format_exc()
                await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
                error = True

            try: # delete vc catergory
                catergory_vc_data = db_bot_data.find_one({"vc_catergory": {"$exists": True}})
                try: catergory_vc = catergory_vc_data["vc_catergory"]
                except: pass

                try: 
                    await interaction.guild.get_channel(catergory_vc).delete()
                    db_bot_data.delete_one({"vc_catergory": catergory_vc})
                except UnboundLocalError: pass
                embed.set_field_at(5, name="Deleting VC Catergory", value=f"**DONE**", inline=True)
            except Exception as e:
                embed.set_field_at(5, name="Deleting VC Catergory", value=f"**FAILED**", inline=True)
                error_traceback = traceback.format_exc()
                await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)
                error = True

            if error == False:
                time_taken = datetime.datetime.strftime(datetime.datetime(1, 1, 1) + (datetime.datetime.utcnow() - started_at), "%M:%S")
                embed.set_footer(text=f"Took {time_taken} to complete")
                embed.title = "UnitedOCE has ended!"
                await interaction.edit_original_message(embed=embed)
                embed = nextcord.Embed(title="UnitedOCE has ended!", color=0x008000)
                embed.set_footer(text=f"Ended by @{interaction.user.name} | Took {time_taken}")
                await interaction.guild.get_channel(channel_bot_event).send(embed=embed)
                formatOutput(output=f"   /{command} was successful!", status="Good")

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_end_Cog(bot))