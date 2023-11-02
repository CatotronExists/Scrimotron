import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, casterRoleID, errorResponse
from Config import db_team_data, db_bot_data

class Command_start_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="start", description="Start UnitedOCE", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def start(self, interaction: nextcord.Interaction):
        command = 'start'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        error = False
        await interaction.response.defer(ephemeral=True)

        try: # build embed
            started_at = datetime.datetime.utcnow()
            teams_processed = 0
            data = list(db_team_data.find())
            embed = nextcord.Embed(title="UnitedOCE is starting!", color=0x000)
            embed.add_field(name="Prepairing", value=f"0%", inline=True)
            embed.add_field(name="Fetching Teams", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Building Roles", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Giving Roles", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Creating VCs", value=f"0/{len(data)}", inline=True)
            embed.add_field(name="Assigning VCs", value=f"0/{len(data)}", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e:
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True

        try: # Make Catergory
            catergory = await interaction.guild.create_category_channel(name="Team VCs", overwrites={interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False), interaction.guild.me: nextcord.PermissionOverwrite(view_channel=True)})
            db_bot_data.insert_one({"vc_catergory": catergory.id})

            embed.set_field_at(0, name="Prepairing", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e:
            embed.set_field_at(0, name="Prepairing", value=f"**FAILED**", inline=True)
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True

        try: # Get teams
            data = list(db_team_data.find())
            embed.set_field_at(1, name="Fetching Teams", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e:
            embed.set_field_at(1, name="Fetching Teams", value=f"**FAILED**", inline=True)
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True

        try: # Make Roles
            for i in data:
                team_name = i["team_name"]
                role = await interaction.guild.create_role(name=team_name, mentionable=True)
                embed.set_field_at(2, name="Building Roles", value=f"{teams_processed}/{len(data)}", inline=True)
                await interaction.edit_original_message(embed=embed)

                db_team_data.update_one(
                    {"team_name": team_name}, 
                    {"$set": {"setup.roleID": role.id}})
                
                teams_processed += 1

            embed.set_field_at(2, name="Building Roles", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e:
            embed.set_field_at(2, name="Building Roles", value=f"**FAILED**", inline=True)
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True

        try: # Assign Roles
            teams_processed = 0
            for i in data:
                team_name = i["team_name"]
                captain = i["captain"]
                player2 = i["player2"]
                player3 = i["player3"]
                sub1 = i["sub1"]
                sub2 = i["sub2"] 
                role1 = interaction.guild.get_role(db_team_data.find_one({"team_name": team_name})["setup"]["roleID"])
                await interaction.guild.get_member(captain).add_roles(role1)
                await interaction.guild.get_member(player2).add_roles(role1)
                await interaction.guild.get_member(player3).add_roles(role1)
                if sub1 != "N/A": await interaction.guild.get_member(sub1).add_roles(role1)
                if sub2 != "N/A": await interaction.guild.get_member(sub2).add_roles(role1)

                embed.set_field_at(3, name="Giving Roles", value=f"{teams_processed}/{len(data)}", inline=True)
                await interaction.edit_original_message(embed=embed)
                teams_processed += 1

            embed.set_field_at(3, name="Giving Roles", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e: 
            embed.set_field_at(3, name="Giving Roles", value=f"**FAILED**", inline=True)
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True

        try: # Make Voice Channels
            teams_processed = 0
            catergory_vc = db_bot_data.find_one({"vc_catergory": {"$exists": True}})["vc_catergory"]
            for i in data:
                team_name = i["team_name"]
                vc = await interaction.guild.create_voice_channel(name=team_name, category=interaction.guild.get_channel(catergory_vc))
                embed.set_field_at(4, name="Creating VCs", value=f"{teams_processed}/{len(data)}", inline=True)
                await interaction.edit_original_message(embed=embed)

                db_team_data.update_one(
                    {"team_name": team_name}, 
                    {"$set": {"setup.channelID": vc.id}})
                teams_processed += 1

            embed.set_field_at(4, name="Creating VCs", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e: 
            embed.set_field_at(4, name="Creating VCs", value=f"**FAILED**", inline=True)
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True

        try: # Assign VCs
            data = list(db_team_data.find())
            teams_processed = 0
            for i in data:
                team_name = i["team_name"]
                vc_id = i["setup"]["channelID"]
                vc = interaction.guild.get_channel(vc_id)
                # get role and give to team members
                role = interaction.guild.get_role(i["setup"]["roleID"])
                casterRole = interaction.guild.get_role(casterRoleID)
                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = True
                overwrite.view_channel = True
                await vc.set_permissions(role, overwrite=overwrite) # allow team to join

                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = True
                overwrite.view_channel = True
                await vc.set_permissions(casterRole, overwrite=overwrite) # allow casters to join

                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = False
                await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite) # deny everyone else

                embed.set_field_at(5, name="Assigning VCs", value=f"{teams_processed}/{len(data)}", inline=True)
                await interaction.edit_original_message(embed=embed)
                teams_processed += 1
            embed.set_field_at(5, name="Assigning VCs", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)
        except Exception as e:
            embed.set_field_at(5, name="Assigning VCs", value=f"**FAILED**", inline=True)
            await errorResponse(error=e, command=command, interaction=interaction)
            error = True
        
        if error == False:
            try: # add time taken
                time_taken = datetime.datetime.strftime(datetime.datetime(1, 1, 1) + (datetime.datetime.utcnow() - started_at), "%M:%S")
                embed.set_footer(text=f"Took {time_taken} to complete")
                embed.title = "UnitedOCE has ended!"
                await interaction.edit_original_message(embed=embed)
                formatOutput(output=f"   /{command} was successful!", status="Good")
            except Exception as e:
                await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_start_Cog(bot))