import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getTeams, getScrimInfo, getConfigData, getChannels, getScrimSetup, DB
from BotData.colors import *

class Command_end_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="end", description="End Scrims. **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def end(self, interaction: nextcord.Interaction):
        global command, userID, guildID
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        started_at = datetime.datetime.utcnow()
        try:
            team_data = getTeams(guildID)
            scrim_info = getScrimInfo(guildID)
            config_data = getConfigData(guildID)
            channels = getChannels(guildID)
            scrim_setup = getScrimSetup(guildID)
            current_pos = 0 # Goes up after each field, allows this to work with this much customization

            embed = nextcord.Embed(title=f"Ending {scrim_info['scrimName']}", color=White)
            embed.add_field(name="Deleting Roles", value=f"0/{len(team_data)}", inline=True)

            if config_data["toggleCheckin"] == True: embed.add_field(name="Deleting Checkins", value=f"0/{len(team_data)}", inline=True)
            if config_data["togglePoi"] == True: embed.add_field(name="Deleting POIs", value=f"0/{len(team_data)}", inline=True)
            if config_data["toggleSetup"] == True: embed.add_field(name="Deleting VCs", value=f"0/{len(team_data)}", inline=True)
            embed.add_field(name="Deleting Team Data", value=f"0/{len(team_data)}", inline=True)
            await interaction.edit_original_message(embed=embed)
            error = False

            try: # delete roles
                teams_processed = 0
                for team in team_data:
                    try: await interaction.guild.get_role(team["teamSetup"]["roleID"]).delete()
                    except: pass

                    DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.roleID": None}})
                    teams_processed += 1
                    embed.set_field_at(current_pos, name="Deleting Roles", value=f"{teams_processed}/{len(team_data)}", inline=True)
                    await interaction.edit_original_message(embed=embed)

                embed.set_field_at(current_pos, name="Deleting Roles", value=f"**DONE**", inline=True)
                await interaction.edit_original_message(embed=embed)
                current_pos += 1

            except Exception as e:
                embed.set_field_at(current_pos, name="Deleting Roles", value=f"**FAILED**", inline=True)
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
                error = True

            if config_data["toggleCheckin"] == True:
                try:
                    channel_checkin = channels["scrimCheckinChannel"]
                    for team in team_data:
                        try:
                            message = await interaction.guild.get_channel(channel_checkin).fetch_message(team["teamSetup"]["checkinMessageID"])
                            await message.delete()
                            DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.checkinMessageID": None}})
                        except: DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.checkinMessageID": None}})
                        teams_processed += 1
                        embed.set_field_at(current_pos, name="Deleting Checkins", value=f"{teams_processed}/{len(team_data)}", inline=True)
                        await interaction.edit_original_message(embed=embed)

                    embed.set_field_at(current_pos, name="Deleting Checkins", value=f"**DONE**", inline=True)
                    await interaction.edit_original_message(embed=embed)
                    current_pos += 1

                except Exception as e:
                    embed.set_field_at(current_pos, name="Deleting Checkins", value=f"**FAILED**", inline=True)
                    error_traceback = traceback.format_exc()
                    await errorResponse(e, command, interaction, error_traceback)
                    error = True

            if config_data["togglePoi"] == True:
                try:
                    channel_poi = channels["scrimPoiChannel"]
                    for team in team_data:
                        try:
                            message = await interaction.guild.get_channel(channel_poi).fetch_message(team["teamSetup"]["poiMessageID"])
                            await message.delete()
                            DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.poiMessageID": None}})
                        except: DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.poiMessageID": None}})
                        teams_processed += 1
                        embed.set_field_at(current_pos, name="Deleting POIs", value=f"{teams_processed}/{len(team_data)}", inline=True)
                        await interaction.edit_original_message(embed=embed)

                    embed.set_field_at(current_pos, name="Deleting POIs", value=f"**DONE**", inline=True)
                    await interaction.edit_original_message(embed=embed)
                    current_pos += 1

                except Exception as e:
                    embed.set_field_at(current_pos, name="Deleting POIs", value=f"**FAILED**", inline=True)
                    error_traceback = traceback.format_exc()
                    await errorResponse(e, command, interaction, error_traceback)
                    error = True

            if config_data["toggleSetup"] == True:
                try:
                    for team in team_data:
                        try:
                            vc = interaction.guild.get_channel(team["teamSetup"]["channelID"])
                            await vc.delete()
                            DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.channelID": None}})
                        except: DB[str(guildID)]["TeamData"].update_one({"teamName": team["teamName"]}, {"$set": {"teamSetup.channelID": None}})
                        teams_processed += 1
                        embed.set_field_at(current_pos, name="Deleting VCs", value=f"{teams_processed}/{len(team_data)}", inline=True)
                        await interaction.edit_original_message(embed=embed)

                    vc_catergory = scrim_setup["vcCatergory"]
                    await interaction.guild.get_channel(vc_catergory).delete()
                    embed.set_field_at(current_pos, name="Deleting VCs", value=f"**DONE**", inline=True)
                    await interaction.edit_original_message(embed=embed)
                    current_pos += 1

                except Exception as e:
                    embed.set_field_at(current_pos, name="Deleting VCs", value=f"**FAILED**", inline=True)
                    error_traceback = traceback.format_exc()
                    await errorResponse(e, command, interaction, error_traceback)
                    error = True

            try: # delete team data
                DB[str(guildID)]["TeamData"].delete_many({})
                embed.set_field_at(current_pos, name="Deleting Team Data", value=f"**DONE**", inline=True)
                await interaction.edit_original_message(embed=embed)
                current_pos += 1

            except Exception as e:
                embed.set_field_at(current_pos, name="Deleting Team Data", value=f"**FAILED**", inline=True)
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
                error = True

            if error == False:
                time_taken = datetime.datetime.strftime(datetime.datetime(1, 1, 1) + (datetime.datetime.utcnow() - started_at), "%M:%S")
                embed.set_footer(text=f"Took {time_taken} to complete")
                embed.title = f"{scrim_info['scrimName']} has ended!"
                await interaction.edit_original_message(embed=embed)
                embed = nextcord.Embed(title=f"{scrim_info['scrimName']} has ended!", color=Green)
                embed.set_footer(text=f"Ended by @{interaction.user.name} | Took {time_taken}")
                await interaction.guild.get_channel(channels["scrimLogChannel"]).send(embed=embed)
                formatOutput(output=f"   /{command} was successful!", status="Good", guildID=guildID)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

def setup(bot):
    bot.add_cog(Command_end_Cog(bot))