import nextcord
import traceback
import time
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getGuildTeams, getDefaults
from Keys import DB
from BotData.colors import *

placeholder_img = "https://github.com/user-attachments/assets/126753ee-e9a9-43d0-a21e-cbc32e555ff2"

class ButtonView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, permission):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.permission = permission

        buttons = {
            "Edit Team Name": {"id": "edit_name", "color": "gray", "Permission": ["Admin", "Captain"]},
            "Edit Team Logo": {"id": "edit_logo", "color": "gray", "Permission": ["Admin", "Captain"]},
            "Modify Team Members": {"id": "modify_members", "color": "red", "Permission": ["Admin", "Captain"]},
            "View Recent Performance": {"id": "view_performance", "color": "main", "Permission": ["Admin", "Captain", "Player", "Sub", "Coach", "Public"]},
            "View Team Stats": {"id": "view_stats", "color": "main", "Permission": ["Admin", "Captain", "Player", "Sub", "Coach", "Public"]},
            "View Logs": {"id": "view_logs", "color": "main", "Permission": ["Admin", "Captain", "Player", "Sub", "Coach", "Public"]},
            "Disband Team": {"id": "disband_team", "color": "red", "Permission": ["Captain"]},
            "Delete Team": {"id": "delete_team", "color": "red", "Permission": ["Admin"]},
            "Leave Team": {"id": "leave_team", "color": "red", "Permission": ["Player", "Sub", "Coach"]},
            "Transfer Captain": {"id": "transfer_captain", "color": "red", "Permission": ["Admin", "Captain"]}
        }

        for label, data in buttons.items():
            if self.permission not in data["Permission"]: continue
            if data["color"] == "gray": button = nextcord.ui.Button(style=nextcord.ButtonStyle.secondary, label=label)
            elif data["color"] == "main": button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label=label)
            elif data["color"] == "green": button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label=label)
            elif data["color"] == "red": button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label=label)
            button.callback = self.create_callback(data["id"])
            self.add_item(button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            try:
                pass # Add logic here
            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())
        return callback

class team_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="team", description="View your team, or lookup a team by name")
    async def team(self, interaction: nextcord.Interaction,
        team_name: str = nextcord.SlashOption(name="team_name", description="Team to search for, leave blank to lookup your team", required=True, autocomplete=True)):

        global command
        command = {'name': interaction.application_command.name, 'guildID': interaction.guild.id, 'userID': interaction.user.id}
        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        try:
            embed = nextcord.Embed(title="Searching for team", description="This may take a few minutes, please wait", color=White)
            await interaction.edit_original_message(embed=embed)

            team_data = getGuildTeams(interaction.guild.id, team_name)
            if not team_data:
                embed = nextcord.Embed(title="Team Not Found", description=f"No team found with the name **{team_name}**", color=Red)
                await interaction.edit_original_message(embed=embed)
                return

            # Permissions | Admin, Captain, Player, Sub, Coach, Public = Everyone Else
            if interaction.user.guild_permissions.administrator: permission = "Admin"
            if interaction.user.id == team_data['teamCaptain']: permission = "Captain"
            elif interaction.user.id == team_data['teamPlayer2']: permission = "Player"
            elif interaction.user.id == team_data['teamPlayer3']: permission = "Player"
            elif interaction.user.id == team_data['teamSub1']: permission = "Sub"
            elif interaction.user.id == team_data['teamSub2']: permission = "Sub"
            elif interaction.user.id == team_data['teamCoach']: permission = "Coach"
            else: permission = "Public"

            embed = nextcord.Embed(title=team_name, description=f"-# Founded at <t:{team_data['createdAt']}:f>", color=White)
            embed.add_field(name="Captain", value=f"<@{team_data['teamCaptain']}>", inline=True)
            embed.add_field(name="Player 2", value=f"<@{team_data['teamPlayer2']}>", inline=True)
            embed.add_field(name="Player 3", value=f"<@{team_data['teamPlayer3']}>", inline=True)
            embed.add_field(name="Sub 1", value=f"<@{team_data['teamSub1']}>" if team_data['teamSub1'] else "-# None", inline=True)
            embed.add_field(name="Sub 2", value=f"<@{team_data['teamSub2']}>" if team_data['teamSub2'] else "-# None", inline=True)
            embed.add_field(name="Coach", value=f"<@{team_data['teamCoach']}>" if team_data['teamCoach'] else "-# None", inline=True)

            try: # Attempt to put team logo in embed, may be expired or changed
                team_logo = team_data['teamLogo']
                embed.set_thumbnail(url=team_logo)

            except:
                team_logo = placeholder_img
                embed.set_thumbnail(url=team_logo)

            await interaction.edit_original_message(embed=embed, view=ButtonView(interaction, permission))

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

    @team.on_autocomplete("team_name")
    async def team_name_autocomplete(self, interaction: nextcord.Interaction, string: str):
        teams = getGuildTeams(interaction.guild.id)
        choices = []
        for team in teams:
            name = team.get("teamName")
            if name and (not string or string.lower() in name.lower()):
                choices.append(name)

        await interaction.response.send_autocomplete(choices[:10])

def setup(bot):
    bot.add_cog(team_Cog(bot))