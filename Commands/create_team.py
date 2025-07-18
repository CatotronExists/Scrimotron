import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse#, getGuildTeams, getDefaults
from BotData.colors import *
import time

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
            "Disband Team": {"id": "disband_team", "color": "red", "Permission": ["Captain"]},
            "Delete Team": {"id": "delete_team", "color": "red", "Permission": ["Admin"]},
            "Leave Team": {"id": "leave_team", "color": "red", "Permission": ["Player", "Sub", "Coach"]},
            "Transfer Captain": {"id": "transfer_captain", "color": "red", "Permission": ["Captain"]}
        }

        for label, data in buttons.items():
            if self.permission not in data["Permission"] and self.permission != "Admin":
                continue
            if data["color"] == "gray":
                button = nextcord.ui.Button(style=nextcord.ButtonStyle.secondary, label=label)
            elif data["color"] == "main":
                button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label=label)
            elif data["color"] == "green":
                button = nextcord.ui.Button(style=nextcord.ButtonStyle.success, label=label)
            elif data["color"] == "red":
                button = nextcord.ui.Button(style=nextcord.ButtonStyle.danger, label=label)
            button.callback = self.create_callback(data["id"])
            self.add_item(button)

    def create_callback(self, custom_id):
        async def callback(interaction: nextcord.Interaction):
            try:
                pass # Add logic here
            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())
        return callback

class create_team_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="create_team", description="Create a team for scrims, generates a team role and dashboard. Creating a team makes you the captain")
    async def create_team(self, interaction: nextcord.Interaction,
        team_name: str = nextcord.SlashOption(name="team_name", description="The name of your team", required=True),
        team_player2: nextcord.Member = nextcord.SlashOption(name="team_player2", description="The second player on your team", required=True),
        team_player3: nextcord.Member = nextcord.SlashOption(name="team_player3", description="The third player on your team", required=True),
        team_sub1: nextcord.Member = nextcord.SlashOption(name="team_sub1", description="The first substitute for your team", required=False),
        team_sub2: nextcord.Member = nextcord.SlashOption(name="team_sub2", description="The second substitute for your team", required=False),
        team_coach: nextcord.Member = nextcord.SlashOption(name="team_coach", description="The coach for your team", required=False),
        team_logo: str = nextcord.SlashOption(name="team_logo", description="The logo for your team, enter a discord image link", required=False)):

        global command
        command = {'name': interaction.application_command.name, 'guildID': interaction.guild.id, 'userID': interaction.user.id}
        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        try:
            embed = nextcord.Embed(title="Validating team...", description="This may take a few minutes, please wait", color=White)
            await interaction.edit_original_message(embed=embed)

            player_ids = set() 
            player_ids.add(interaction.user.id)
            player_ids.add(team_player2.id)
            player_ids.add(team_player3.id)
            if team_sub1: player_ids.add(team_sub1.id)
            if team_sub2: player_ids.add(team_sub2.id)
            if team_coach: player_ids.add(team_coach.id)

            # Check if a user is listed multiple times
            if len(player_ids) < 3 + (1 if team_sub1 else 0) + (1 if team_sub2 else 0) + (1 if team_coach else 0):
                embed = nextcord.Embed(title="Team Creation Error", description="You cannot have the same player listed multiple times!", color=Red)
                await interaction.edit_original_message(embed=embed)
                return

            # Check if team is valid (name, players, etc.)
            teams = getGuildTeams(interaction.guild.id)

            bot_list = checks = []
            if team_player2.bot == True: bot_list.append(str(team_player2.name))
            if team_player3.bot == True: bot_list.append(str(team_player3.name))
            if team_sub1 and team_sub1.bot == True: bot_list.append(str(team_sub1.name))
            if team_sub2 and team_sub2.bot == True: bot_list.append(str(team_sub2.name))
            if team_coach and team_coach.bot == True: bot_list.append(str(team_coach.name))

            if len(bot_list) > 0:
                embed = nextcord.Embed(title="Team Creation Error", description=f"The following users are bots and cannot be added to teams:\n{'\n'.join(bot_list)}", color=Red)
                await interaction.edit_original_message(embed=embed)
                return

            for team in teams:
                if team["teamName"].lower() == team_name.lower(): # Check if name is taken
                    embed = nextcord.Embed(title="Team Creation Error", description=f"Team name: **{team_name}** is already taken!", color=Red)
                    await interaction.edit_original_message(embed=embed)
                    return

                current_team_players = [team["teamCaptain"], team["teamPlayer2"], team["teamPlayer3"]]
                if team_sub1: current_team_players.append(team["teamSub1"])
                if team_sub2: current_team_players.append(team["teamSub2"])
                if team_coach: current_team_players.append(team["teamCoach"])

                for player_id in player_ids:
                    if player_id in current_team_players:
                        checks.append(player_id)

            if len(checks) > 0: # If any of the players are already in a team
                embed = nextcord.Embed(title="Team Creation Error", description=f"The following users are already in a team:\n{', '.join(f'<@{id}>' for id in checks)}", color=Red)
                await interaction.edit_original_message(embed=embed)
                return

            embed = nextcord.Embed(title="Creating team...", description="This may take a few minutes, please wait", color=White)
            await interaction.edit_original_message(embed=embed)

            permission = "Captain"
            # Permissions | Admin, Captain, Player, Sub, Coach, Public = Everyone Else

            created_time = int(time.time())
            embed = nextcord.Embed(title=team_name, description=f"-# Founded at <t:{created_time}:f>", color=White)
            embed.add_field(name="Captain", value=interaction.user.mention, inline=True)
            embed.add_field(name="Player 2", value=team_player2.mention, inline=True)
            embed.add_field(name="Player 3", value=team_player3.mention, inline=True)
            embed.add_field(name="Sub 1", value=team_sub1.mention if team_sub1 else "-# None", inline=True)
            embed.add_field(name="Sub 2", value=team_sub2.mention if team_sub2 else "-# None", inline=True)
            embed.add_field(name="Coach", value=team_coach.mention if team_coach else "-# None", inline=True)
            if team_logo: # If no logo is provided, use a default image
                if team_logo.startswith("https://cdn.discordapp.com/attachments/"):
                    embed.set_thumbnail(url=team_logo)

                    # Discord deletes images after 24 hours, new system is required

                else: 
                    embed.set_thumbnail(url=placeholder_img)

            else: embed.set_thumbnail(url=placeholder_img)
            await interaction.edit_original_message(embed=embed, view=ButtonView(interaction, permission))

            # Save team data to database
            template = getDefaults("Team")["Team"]

            template["teamName"] = team_name
            template["teamCaptain"] = interaction.user.id
            template["teamPlayer2"] = team_player2.id
            template["teamPlayer3"] = team_player3.id
            if team_sub1: template["teamSub1"] = team_sub1.id
            if team_sub2: template["teamSub2"] = team_sub2.id
            if team_coach: template["teamCoach"] = team_coach.id
            template["createdAt"] = created_time
            template["teamLogo"] = team_logo
            template = {team_name: template}

            DB[str(interaction.guild.id)]["Teams"].insert_one(template)

            embed = nextcord.Embed(title="Team created successfully!", description=f"Your team **{team_name}** has been created.\nYou can now manage your team via `/team`", color=Green)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

def setup(bot):
    bot.add_cog(create_team_Cog(bot))