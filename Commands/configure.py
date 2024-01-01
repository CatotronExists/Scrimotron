import nextcord
import datetime
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_bot_event
from Config import db_bot_data

class Command_configure_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="configure", description="Configure the bot")
    async def configure(self, interaction: nextcord.Interaction):
        global command
        command = 'configure'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")

        data = db_bot_data.find_one({"AutoEvent": {"$exists": True}})

        embed = nextcord.Embed(title="Bot Config", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
        embed.add_field(name="Auto Setup", value=data["AutoEvent"]["Setup"])
        embed.add_field(name="Auto Checkin", value=data["AutoEvent"]["Checkin"])
        embed.add_field(name="Auto Poi Selection", value=data["AutoEvent"]["Poi"])
        embed.add_field(name="Check Delay", value=data["AutoEvent"]["Delay"])

        await interaction.send(embed=embed, ephemeral=True, view=Command_configure_Cog.main_view(interaction))

    class main_view (nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction):
            super().__init__(timeout=None)
            self.interaction = interaction
            data = db_bot_data.find_one({"AutoEvent": {"$exists": True}})

            for i in data["AutoEvent"]:
                button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.blurple)
                button.callback = self.create_callback(i)
                self.add_item(button)
        
        def create_callback(self, i):
            async def callback(interaction: nextcord.Interaction):
                data = db_bot_data.find_one({"AutoEvent": {"$exists": True}})
                embed = nextcord.Embed(title=f"Editing {i}", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
                embed.add_field(name="Auto Setup", value=data["AutoEvent"]["Setup"])
                await interaction.send(embed=embed, view=Command_configure_Cog.sub_view(interaction, i), ephemeral=True)
            return callback
    
    class sub_view (nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, i):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.i = i

            actions = ["-10", "-1", "Confirm", "+1", "+10"]

            for item in actions:
                button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.blurple)
                button.callback = self.create_callback(item, i)
                self.add_item(button)
        
        def create_callback(self, item, i):
            async def callback(interaction: nextcord.Interaction):
                try:
                    data = db_bot_data.find_one({"AutoEvent": {"$exists": True}})
                    old_value = data["AutoEvent"][i]

                    if item == "-10": new_value = data["AutoEvent"][i] - 10
                    elif item == "-1": new_value = data["AutoEvent"][i] - 1
                    elif item == "Confirm": new_value = data["AutoEvent"][i]
                    elif item == "+1": new_value = data["AutoEvent"][i] + 1
                    elif item == "+10": new_value = data["AutoEvent"][i] + 10

                    db_bot_data.update_one({"AutoEvent": {"$exists": True}}, {"$set": {f"AutoEvent.{i}": new_value}})

                    errors = 0
                    if new_value < 0: 
                        new_value = old_value
                        embed = nextcord.Embed(title=f"Error", description=f"⛔{i} Cannot be less than 0", color=0xFF0000)
                        await interaction.send(embed=embed, ephemeral=True)
                        db_bot_data.update_one({"AutoEvent": {"$exists": True}}, {"$set": {f"AutoEvent.{i}": old_value}})

                        embed = nextcord.Embed(title=f"Editing {i}", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
                        embed.add_field(name="Auto Setup", value=new_value)
                        await interaction.send(embed=embed, view=Command_configure_Cog.sub_view(interaction, i), ephemeral=True)
                        errors = errors + 1
                    
                    if i == "Delay":
                        if new_value < 0 or new_value > 60:
                            embed = nextcord.Embed(title=f"Error", description="⛔Delay Cannot be less than 0 or more than 60", color=0xFF0000)
                            await interaction.send(embed=embed, ephemeral=True)
                            db_bot_data.update_one({"AutoEvent": {"$exists": True}}, {"$set": {f"AutoEvent.{i}": old_value}})

                            embed = nextcord.Embed(title=f"Editing {i}", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
                            embed.add_field(name="Auto Setup", value=new_value)
                            await interaction.send(embed=embed, view=Command_configure_Cog.sub_view(interaction, i), ephemeral=True)
                            errors = errors + 1
                            pass
                        else: pass

                    if i == "Setup": 
                        if data["AutoEvent"]["Checkin"] < new_value or data["AutoEvent"]["Poi"] < new_value:
                            embed = nextcord.Embed(title=f"Error", description="⛔Setup Cannot be more than Checkin or Poi ", color=0xFF0000)
                            await interaction.send(embed=embed, ephemeral=True)
                            db_bot_data.update_one({"AutoEvent": {"$exists": True}}, {"$set": {f"AutoEvent.{i}": old_value}})

                            embed = nextcord.Embed(title=f"Editing {i}", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
                            embed.add_field(name="Auto Setup", value=new_value)
                            await interaction.send(embed=embed, view=Command_configure_Cog.sub_view(interaction, i), ephemeral=True)
                            errors = errors + 1
                            pass
                        else: pass

                    if errors == 0:
                        if item != "Confirm":
                            embed = nextcord.Embed(title=f"Editing {i}", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
                            embed.add_field(name="Auto Setup", value=new_value)
                            await interaction.send(embed=embed, view=Command_configure_Cog.sub_view(interaction, i), ephemeral=True)
                        elif item == "Confirm":
                            embed = nextcord.Embed(title="Bot Config", description="Change the Bot settings with the buttons\nAuto (item) is displayed in hours *eg. Auto Setup - 1 (1 Hour)*", color=0x000)
                            embed.add_field(name="Auto Setup", value=data["AutoEvent"]["Setup"])
                            embed.add_field(name="Auto Checkin", value=data["AutoEvent"]["Checkin"])
                            embed.add_field(name="Auto Poi Selection", value=data["AutoEvent"]["Poi"])
                            embed.add_field(name="Check Delay", value=data["AutoEvent"]["Delay"])
                            await interaction.send(embed=embed, view=Command_configure_Cog.main_view(interaction), ephemeral=True)

                            if old_value != new_value: # send log if changed
                                channel = interaction.guild.get_channel(channel_bot_event)
                                embed = nextcord.Embed(title="Bot Config Changed", description=f"`{i}` Changed to {new_value}, from {old_value}", color=0x008000)
                                embed.set_footer(text=f"Changes may take up to 5 minutes to take affect! Changed by @{interaction.user.name}")
                                await channel.send(embed=embed)
                    else: pass
                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)   
            return callback

def setup(bot):
    bot.add_cog(Command_configure_Cog(bot))