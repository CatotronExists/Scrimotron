import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID
from Config import db_team_data, db_bot_data

class Command_start_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

@nextcord.slash_command(guild_ids=[guildID], name="start", description="Start UnitedOCE")
async def start(self, interaction: nextcord.Interaction):
    command = 'start'
    userID = interaction.user.id
    formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
    teams_processed = 0
    error = False
    error_count = 0
    await interaction.response.defer(ephemeral=True)
    data = list(db_team_data.find())
    embed = nextcord.Embed(title="UnitedOCE is starting!", color=0x000)
    embed.add_field(name="Prepairing", value=f"0%", inline=True)
    embed.add_field(name="Fetching Teams", value=f"0/{len(data)}", inline=True)
    embed.add_field(name="Building Roles", value=f"0/{len(data)}", inline=True)
    embed.add_field(name="Giving Roles", value=f"0/{len(data)}", inline=True)
    embed.add_field(name="Creating VCs", value=f"0/{len(data)}", inline=True)
    embed.add_field(name="Assigning VCs", value=f"0/{len(data)}", inline=True)
    await interaction.edit_original_message(embed=embed)
    
    # Make Catergory & participant role
    if error == False:
        try: 
            catergory = await interaction.guild.create_category_channel(name="Team VCs", overwrites={interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False), interaction.guild.me: nextcord.PermissionOverwrite(view_channel=True)})
            db_bot_data.insert_one({"vc_catergory": catergory.id})

            role = await interaction.guild.create_role(name="UnitedOCE Participant", mentionable=True)
            db_bot_data.insert_one({"participant_role": role.id})

            embed.set_field_at(0, name="Prepairing", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)

        except Exception as e: 
            formatOutput(output=f"FAILED TO CREATE Catergory & Role, {e}", status="Error")
            error = True
            error_count += 1
    elif error == True:
        embed.set_field_at(0, name="Prepairing", value=f"**FAILED**", inline=True)
        embed.add_field(name="Errors", value=f"{error_count}", inline=True)
        await interaction.edit_original_message(embed=embed)
        await interaction.followup.send(content=f"Full list of errors: {e}")

    # Get teams
    if error == False:
        try:
            data = list(db_team_data.find())
            embed.set_field_at(1, name="Fetching Teams", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)

        except Exception as e: 
            formatOutput(output=f"FAILED TO Get Teams, {e}", status="Error")
            error = True
            error_count += 1
    elif error == True:
        embed.set_field_at(1, name="Fetching Teams", value=f"**FAILED**", inline=True)
        embed.add_field(name="Errors", value=f"{error_count}", inline=True)
        await interaction.edit_original_message(embed=embed)
        await interaction.followup.send(content=f"Full list of errors: {e}")

    # Make Roles
    if error == False:
        teams_processed = 0
        try:
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
            formatOutput(output=f"FAILED TO CREATE Roles, {e}", status="Error")
            error = True
            error_count += 1
    elif error == True:
        embed.set_field_at(2, name="Building Roles", value=f"**FAILED**", inline=True)
        embed.add_field(name="Errors", value=f"{error_count}", inline=True)
        await interaction.edit_original_message(embed=embed)
        await interaction.followup.send(content=f"Full list of errors: {e}")

    # Assign Roles
    if error == False:
        try:
            teams_processed = 0
            for i in data:
                team_name = i["team_name"]
                captain = i["captain"]
                player2 = i["player2"]
                player3 = i["player3"]
                sub1 = i["sub1"]
                sub2 = i["sub2"] 
                role1 = interaction.guild.get_role(db_team_data.find_one({"team_name": team_name})["setup"]["roleID"])
                role2 = interaction.guild.get_role(db_bot_data.find_one({"participant_role": {"$exists": True}})["participant_role"])
                await interaction.guild.get_member(captain).add_roles(role1, role2)
                await interaction.guild.get_member(player2).add_roles(role1, role2)
                await interaction.guild.get_member(player3).add_roles(role1, role2)
                if sub1 != "N/A": await interaction.guild.get_member(sub1).add_roles(role1, role2)
                if sub2 != "N/A": await interaction.guild.get_member(sub2).add_roles(role1, role2)

                embed.set_field_at(3, name="Giving Roles", value=f"{teams_processed}/{len(data)}", inline=True)
                await interaction.edit_original_message(embed=embed)
                teams_processed += 1

            embed.set_field_at(3, name="Giving Roles", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)

        except Exception as e: 
            formatOutput(output=f"FAILED TO ASSIGN Roles, {e}", status="Error")
            error = True
            error_count += 1
    elif error == True:
        embed.set_field_at(3, name="Giving Roles", value=f"**FAILED**", inline=True)
        embed.add_field(name="Errors", value=f"{error_count}", inline=True)
        await interaction.edit_original_message(embed=embed)
        await interaction.followup.send(content=f"Full list of errors: {e}")

    # Make Voice Channels
    if error == False:
        try:
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
            formatOutput(output=f"FAILED TO CREATE VCs, {e}", status="Error")
            error = True
            error_count += 1
    elif error == True:
        embed.set_field_at(4, name="Creating VCs", value=f"**FAILED**", inline=True)
        embed.add_field(name="Errors", value=f"{error_count}", inline=True)
        await interaction.edit_original_message(embed=embed)
        await interaction.followup.send(content=f"Full list of errors: {e}")

    # Assign VCs
    if error == False:
        try:
            data = list(db_team_data.find())
            teams_processed = 0
            for i in data:
                team_name = i["team_name"]
                vc_id = i["setup"]["channelID"]
                vc = interaction.guild.get_channel(vc_id)
                # get role and give to team members
                role = interaction.guild.get_role(i["setup"]["roleID"])
                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = True
                overwrite.view_channel = True
                await vc.set_permissions(role, overwrite=overwrite) # allow team to join

                overwrite = nextcord.PermissionOverwrite()
                overwrite.connect = False
                await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite) # deny everyone else

                embed.set_field_at(5, name="Assigning VCs", value=f"{teams_processed}/{len(data)}", inline=True)
                await interaction.edit_original_message(embed=embed)
                teams_processed += 1
            embed.set_field_at(5, name="Assigning VCs", value=f"**DONE**", inline=True)
            await interaction.edit_original_message(embed=embed)

        except Exception as e:
            formatOutput(output=f"FAILED TO ASSIGN VCs, {e}", status="Error")
            error = True
            error_count += 1
    elif error == True:
        embed.set_field_at(5, name="Assigning VCs", value=f"**FAILED**", inline=True)
        embed.add_field(name="Errors", value=f"{error_count}", inline=True)
        await interaction.edit_original_message(embed=embed)
        await interaction.followup.send(content=f"Full list of errors: {e}")

def setup(bot):
    bot.add_cog(Command_start_Cog(bot))