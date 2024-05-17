from discord import TextInputStyle
import time
import datetime
import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getConfigData, getChannels, getScrimInfo, getMessages, DB, splitMessage, unformatMessage
from BotData.colors import *
from BotData.configurationdata import ConfigData

class set_log_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        button = nextcord.ui.Button(label="Set", style=nextcord.ButtonStyle.blurple)
        button.callback = self.create_callback()
        self.add_item(button)

    def create_callback(self):
        async def callback(interaction: nextcord.Interaction):
            try:
                await interaction.response.send_modal(modal=set_log_modal(interaction))

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class set_log_modal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__("Channel ID", timeout=None)
        self.interaction = interaction

        self.input = nextcord.ui.TextInput(
            label="Channel ID",
            placeholder="Enter Channel ID",
            min_length=0,
            max_length=20)

        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        config_data = getConfigData(interaction.guild.id)
        messages = getMessages(interaction.guild.id)
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                channel = interaction.guild.get_channel(response)
                if channel == None: # Channel Not Found
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Set**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"\n\n**ERROR** | Channel ID Must Be A Valid Channel", color=Red)
                    await interaction.send(embed=embed, view=set_log_view(interaction), ephemeral=True)

                else:
                    DB[str(interaction.guild.id)]["Config"].update_one({"channels": {"$exists": True}}, {"$set": {f"channels.scrimLogChannel": response}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**Channels -> Log -> Change Channel** Set To <#{response}>", color=Green)
                    await interaction.send(embed=embed, ephemeral=True)

                    formatOutput(output=f"Channels Log Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    await channel.send(embed=embed)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Set**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"\n\n**ERROR** | Channel ID Must Be A Numerical Value (e.g 123456789)", color=Red)
                await interaction.send(embed=embed, view=set_log_view(interaction), ephemeral=True)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

class main_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        for option in ConfigData.keys():
            button = nextcord.ui.Button(label=option, style=nextcord.ButtonStyle.blurple)
            button.callback = self.create_callback(option)
            self.add_item(button)

        button = nextcord.ui.Button(label="RESET", style=nextcord.ButtonStyle.danger)
        button.callback = self.create_callback("RESET")
        self.add_item(button)

    def create_callback(self, option):
        async def callback(interaction: nextcord.Interaction):
            try:
                config_data = getConfigData(interaction.guild.id)
                messages = getMessages(interaction.guild.id)
                channels = getChannels(interaction.guild.id)
                if option != "RESET": # Not Reset
                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option}", description=f"Change {option} Options", color=White)
                    for sub_option in ConfigData[option]:
                        if ConfigData[option][sub_option]["ValueID"] == 1: value = f"{config_data[f'toggle{sub_option}']} | Set to {config_data[f'toggle{sub_option}Time']} hour(s) before start"

                        elif ConfigData[option][sub_option]["ValueID"] == 2:
                            if config_data['casterRole'] == None: value = f"{config_data['caster']} | Role: **Not Set**"
                            else: value = f"{config_data['caster']} | Role: <@&{config_data['casterRole']}>"

                        elif ConfigData[option][sub_option]["ValueID"] == 3:
                            default_message = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"][f"scrim{sub_option}"]
                            if messages[f'scrim{sub_option}'] == default_message: value = "**Default Message** | Click to View/Edit"
                            else: value = f"**Custom Message** | Click to View/Edit"

                        elif ConfigData[option][sub_option]["ValueID"] == 4:
                            if channels[f"scrim{sub_option}Channel"] == None: value = "**Not Set**"
                            else: value = f"<#{channels[f'scrim{sub_option}Channel']}>"

                        embed.add_field(name=sub_option, value=value, inline=False)
                    await interaction.send(embed=embed, view=sub_view(interaction, option), ephemeral=True)

                else:
                    embed = nextcord.Embed(title="**RESET CONFIG DATA?**", description="Are you sure you want to reset all config data?\n*Only log channel settings will remain!*", color=Red)
                    await interaction.send(embed=embed, view=reset_view(interaction, option), ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class sub_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option

        for sub_option in ConfigData[option]:
            button = nextcord.ui.Button(label=sub_option, style=nextcord.ButtonStyle.blurple)
            button.callback = self.create_callback(sub_option)
            self.add_item(button)

        button = nextcord.ui.Button(label="Back", style=nextcord.ButtonStyle.grey)
        button.callback = self.create_callback("Back")
        self.add_item(button)

    def create_callback(self, sub_option):
        async def callback(interaction: nextcord.Interaction):
            try:
                if sub_option == "Back":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                else:
                    config_data = getConfigData(interaction.guild.id)
                    messages = getMessages(interaction.guild.id)
                    channels = getChannels(interaction.guild.id)
                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {self.option} -> {sub_option}", description=f"Change {sub_option} Options", color=White)
                    if ConfigData[self.option][sub_option]["ValueID"] == 1: value = f"{config_data[f'toggle{sub_option}']} | Set to {config_data[f'toggle{sub_option}Time']} hour(s) before start"

                    elif ConfigData[self.option][sub_option]["ValueID"] == 2:
                        if config_data['casterRole'] == None: value = f"{config_data['caster']} | Role: **Not Set**"
                        else: value = f"{config_data['caster']} | Role: <@&{config_data['casterRole']}>"

                    elif ConfigData[self.option][sub_option]["ValueID"] == 3:
                        if messages[f'scrim{sub_option}'] == DB.Scrimotron.GlobalData["defaultMessages"][f"scrim{sub_option}"]: value = "**Default Message** | Click to View/Edit"
                        else: value = f"**Custom Message** | Click to View/Edit"

                    elif ConfigData[self.option][sub_option]["ValueID"] == 4:
                        if channels[f"scrim{sub_option}Channel"] == None: value = "**Not Set**"
                        else: value = f"<#{channels[f'scrim{sub_option}Channel']}>"

                    embed.add_field(name=sub_option, value=value, inline=False)
                    await interaction.send(embed=embed, view=sub_sub_view(interaction, self.option, sub_option), ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class sub_sub_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option, sub_option):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option

        config_data = getConfigData(interaction.guild.id)
        messages = getMessages(interaction.guild.id)
        channels = getChannels(interaction.guild.id)

        for button_label in ConfigData[option][sub_option]["Buttons"]:
            if button_label == "Enable":
                if ConfigData[option][sub_option]["ValueID"] == 1:
                    if config_data[f'toggle{sub_option}'] == False: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.success)
                    else: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.success, disabled=True)

                elif ConfigData[option][sub_option]["ValueID"] == 2:
                    if config_data['caster'] == False: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.success)
                    else: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.success, disabled=True)

            elif button_label == "Disable":
                if ConfigData[option][sub_option]["ValueID"] == 1:
                    if config_data[f'toggle{sub_option}'] == True: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.danger)
                    else: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.danger, disabled=True)

                elif ConfigData[option][sub_option]["ValueID"] == 2:
                    if config_data['caster'] == True: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.danger)
                    else: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.danger, disabled=True)
            else:
                button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.blurple)

            button.callback = self.create_callback(button_label, option, sub_option)
            self.add_item(button)

        button = nextcord.ui.Button(label="Back", style=nextcord.ButtonStyle.grey)
        button.callback = self.create_callback("Back", option, sub_option)
        self.add_item(button)

    def create_callback(self, action, option, sub_option):
        async def callback(interaction: nextcord.Interaction):
            config_data = getConfigData(interaction.guild.id)
            messages = getMessages(interaction.guild.id)
            channels = getChannels(interaction.guild.id)
            try:
                if action == "Back":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                else:
                    if action == "Enable":
                        if ConfigData[option][sub_option]["ValueID"] == 1:
                            DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {f"config.toggle{sub_option}": True}})
                        elif ConfigData[option][sub_option]["ValueID"] == 2:
                            DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {"config.caster": True}})

                        embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option}** set to {action}", color=Green)
                        await interaction.send(embed=embed, ephemeral=True)
                        formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                        embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                        channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                        await channel.send(embed=embed)

                    elif action == "Disable":
                        if ConfigData[option][sub_option]["ValueID"] == 1:
                            DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {f"config.toggle{sub_option}": False}})
                        elif ConfigData[option][sub_option]["ValueID"] == 2:
                            DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {"config.caster": False}})

                        embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option}** set to {action}", color=Green)
                        await interaction.send(embed=embed, ephemeral=True)
                        formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                        embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                        channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                        await channel.send(embed=embed)

                    elif action == "Change Timing":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Timing", color=White)
                        embed.add_field(name=sub_option, value=f"Set to **{config_data[f"toggle{sub_option}Time"]}** hour(s) before start", inline=False)
                        await interaction.send(embed=embed, view=change_timing_view(interaction, option, sub_option, action), ephemeral=True)

                    elif action == "Change Channel":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Channel", color=White)
                        if channels[f"scrim{sub_option}Channel"] == None: embed.add_field(name=sub_option, value="**Not Set**", inline=False)
                        else: embed.add_field(name=sub_option, value=f"Set to <#{channels[f'scrim{sub_option}Channel']}>", inline=False)
                        await interaction.response.send_modal(modal=change_channel_view(interaction, option, sub_option, action))

                    elif action == "Change Message":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Message", color=White)
                        if messages[f'scrim{sub_option}'] == DB.Scrimotron.GlobalData["defaultMessages"][f"scrim{sub_option}"]: embed.add_field(name=sub_option, value="**Default Message** | Click to View/Edit", inline=False)
                        else: embed.add_field(name=sub_option, value="**Custom Message** | Click to View/Edit", inline=False)
                        await interaction.send(embed=embed, view=change_message_view(interaction, option, sub_option, action), ephemeral=True)

                    elif action == "Change Role":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Role", color=White)
                        if config_data['casterRole'] == None: embed.add_field(name=sub_option, value="**Not Set**", inline=False)
                        else: embed.add_field(name=sub_option, value=f"Set to <@&{config_data['casterRole']}>", inline=False)
                        await interaction.response.send_modal(modal=change_role_modal(interaction, option, sub_option, action))

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class change_timing_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option, sub_option, action):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        actions = ["-3", "-1", "+1", "+3", "Confirm", "Cancel"]

        for item in actions:
            if item == "Confirm": button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.success)
            elif item == "Cancel": button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.danger)
            else: button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.blurple)
            button.callback = self.create_callback(option, sub_option, action, pressed=item)
            self.add_item(button)

    def create_callback(self, option, sub_option, action, pressed):
        async def callback(interaction: nextcord.Interaction):
            config_data = getConfigData(interaction.guild.id)
            messages = getMessages(interaction.guild.id)
            channels = getChannels(interaction.guild.id)
            try:
                previous_setting = config_data[f'toggle{self.sub_option}Time']
                if pressed == "Cancel":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif pressed == "Confirm":
                    if previous_setting < 0 or previous_setting == 0:
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="**ERROR** | Time Cannot Be Less Than One Hour", color=Red)
                        await interaction.send(embed=embed, ephemeral=True)
                        return

                    else:
                        DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {f"config.toggle{sub_option}Time": previous_setting}})

                        embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{option} -> {sub_option} -> {action}** Set To {previous_setting}", color=Green)
                        await interaction.send(embed=embed, ephemeral=True)
                        formatOutput(output=f"{option} {sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                        embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                        channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                        await channel.send(embed=embed)

                else:
                    if pressed == "-3": new_setting = previous_setting - 3
                    elif pressed == "-1": new_setting = previous_setting - 1
                    elif pressed == "+1": new_setting = previous_setting + 1
                    elif pressed == "+3": new_setting = previous_setting + 3

                    DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {f"config.toggle{sub_option}Time": new_setting}})

                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Timing", color=White)
                    embed.add_field(name=sub_option, value=f"Set to **{new_setting}** hour(s) before start", inline=False)
                    await interaction.send(embed=embed, view=change_timing_view(interaction, option, sub_option, action), ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class change_channel_view(nextcord.ui.Modal):
    def __init__(self, interaction, option, sub_option, action):
        super().__init__("Channel ID", timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        self.input = nextcord.ui.TextInput(
            label="Channel ID",
            placeholder="Enter Channel ID",
            min_length=0,
            max_length=20)

        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        config_data = getConfigData(interaction.guild.id)
        messages = getMessages(interaction.guild.id)
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                channel = interaction.guild.get_channel(response)
                if channel == None:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n**ERROR** | Channel ID Must Be A Valid Channel", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                else:
                    DB[str(interaction.guild.id)]["Config"].update_one({"channels": {"$exists": True}}, {"$set": {f"channels.scrim{self.sub_option}Channel": response}})

                    if self.sub_option != "Log": # Ignoring log channel changes
                        scrim_info = getScrimInfo(interaction.guild.id)

                        if self.sub_option == "Announcement": # If announcement channel is changed
                            if scrim_info["scrimEpoch"].isnumeric() == True: # A scrim has been scheduled before
                                scrim_epoch = int(scrim_info["scrimEpoch"])

                                if scrim_epoch > time.time(): # Scrim has already started/ended
                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Channel Updated To <#response>, Announcement Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                else: # Scrim has not started yet
                                    message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                    message_split = message.split("\n")
                                    title = message_split[0]
                                    description = '\n'.join(message_split[1:])

                                    embed = nextcord.Embed(title=title, description=description, color=White)
                                    await channel.send(embed=embed)

                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Channel Updated To <#response>, Announcement Message Moved", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # No scrims have ever been scheduled
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Channel Updated To <#response>, Announcement Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        elif self.sub_option == "Checkin": # If checkin channel is changed
                            if config_data['toggleCheckin'] == True: # Checkins are enabled
                                if scrim_info["scrimEpoch"].isnumeric() == True:
                                    scrim_epoch = int(scrim_info["scrimEpoch"])
                                    if scrim_epoch > time.time():
                                        scrim_datetime = datetime.datetime.fromtimestamp(scrim_epoch)
                                        current_datetime = datetime.datetime.now()
                                        time_until_start = scrim_datetime - current_datetime
                                        hours_until_start = time_until_start.total_seconds() / 3600

                                        if hours_until_start < config_data['toggleCheckinTime']: # If it is time to open checkins
                                            message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                            message_split = message.split("\n")
                                            title = message_split[0]
                                            description = '\n'.join(message_split[1:])

                                            embed = nextcord.Embed(title=title, description=description, color=White)
                                            await channel.send(embed=embed)

                                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Channel Updated To <#response>, Checkin Message Moved", color=White)
                                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                        else: # Not time to open checkins
                                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Channel Updated To <#response>, Checkin Message Not Sent (Checkins Not Open)", color=White)
                                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                    else: # Scrims have already started/ended
                                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Channel Updated To <#response>, Checkin Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                else: # No scrims have ever been scheduled
                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Channel Updated To <#response>, Checkin Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # Checkins are disabled
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Channel Updated To <#response>, Checkin Message Not Sent (Checkins Disabled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        elif self.sub_option == "Rules": # If rules channel is changed
                            message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                            message_split = message.split("\n")
                            title = message_split[0]
                            description = '\n'.join(message_split[1:])

                            embed = nextcord.Embed(title=title, description=description, color=White)
                            await channel.send(embed=embed)

                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRules Channel Updated To <#response>, Rules Message Moved", color=White)
                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        elif self.sub_option == "Format": # If format channel is changed
                            message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                            message_split = message.split("\n")
                            title = message_split[0]
                            description = '\n'.join(message_split[1:])

                            embed = nextcord.Embed(title=title, description=description, color=White)
                            await channel.send(embed=embed)

                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nFormat Channel Updated To <#response>, Format Message Moved", color=White)
                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        elif self.sub_option == "Poi": # If poi channel is changed
                            if config_data['togglePoi'] == True: # Poi selection is enabled
                                if scrim_info["scrimEpoch"].isnumeric() == True:
                                    scrim_epoch = int(scrim_info["scrimEpoch"])
                                    if scrim_epoch > time.time():
                                        scrim_datetime = datetime.datetime.fromtimestamp(scrim_epoch)
                                        current_datetime = datetime.datetime.now()
                                        time_until_start = scrim_datetime - current_datetime
                                        hours_until_start = time_until_start.total_seconds() / 3600

                                        if hours_until_start < config_data['togglePoiTime']: # If it is time to open poi selection
                                            message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                            message_split = message.split("\n")
                                            title = message_split[0]
                                            description = '\n'.join(message_split[1:])

                                            embed = nextcord.Embed(title=title, description=description, color=White)
                                            await channel.send(embed=embed)

                                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Channel Updated To <#response>, Poi Message Moved", color=White)
                                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                        else: # Not time to open poi selection
                                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Channel Updated To <#response>, Poi Message Not Sent (Poi Selection Not Open)", color=White)
                                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                    else: # Scrims have already started/ended
                                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Channel Updated To <#response>, Poi Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                else: # No scrims have ever been scheduled
                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Channel Updated To <#response>, Poi Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # Poi selection is disabled
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Channel Updated To <#response>, Poi Message Not Sent (Poi Selection Disabled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        elif self.sub_option == "Registration": # If registration channel is changed
                            if scrim_info["scrimEpoch"].isnumeric() == True: # A scrim has been scheduled before
                                scrim_epoch = int(scrim_info["scrimEpoch"])

                                if scrim_epoch > time.time(): # Scrim has already started/ended
                                    message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                    message_split = message.split("\n")
                                    title = message_split[0]
                                    description = '\n'.join(message_split[1:])

                                    embed = nextcord.Embed(title=title, description=description, color=White)
                                    await channel.send(embed=embed)

                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Channel Updated To <#response>, Registration Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                else:
                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Channel Updated To <#response>, Registration Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # No scrims have ever been scheduled
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Channel Updated To <#response>, Registration Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action}** Set To <#{response}>", color=Green)
                    await interaction.send(embed=embed, ephemeral=True)
                    formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    if self.sub_option == "Log": channel = interaction.guild.get_channel(response)
                    else: channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n **ERROR** | Channel ID Must Be A Numerical Value (e.g 123456789)", color=White)
                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

class change_message_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option, sub_option, action):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        actions = ["View", "Edit", "Reset", "Back"]

        for item in actions:
            if item == "View": button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.blurple)
            elif item == "Edit": button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.blurple)
            elif item == "Reset": button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.danger)
            else: button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.grey)
            button.callback = self.create_callback(option, sub_option, action, item)
            self.add_item(button)

    def create_callback(self, option, sub_option, action, pressed):
        async def callback(interaction: nextcord.Interaction):
            config_data = getConfigData(interaction.guild.id)
            messages = getMessages(interaction.guild.id)
            channels = getChannels(interaction.guild.id)
            try:
                if pressed == "Cancel":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif pressed == "Reset":
                    default_message = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"][f"scrim{sub_option}"]
                    DB[str(interaction.guild.id)]["Messages"].update_one({"messages": {"$exists": True}}, {"$set": {f"messages.scrim{sub_option}": default_message}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{option} -> {sub_option} -> {action}** Reset To Default Message", color=Green)
                    await interaction.send(embed=embed, ephemeral=True)
                    formatOutput(output=f"{option} {sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{option} -> {sub_option} -> {action}** Reset To Default Message", color=Green)
                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

                elif pressed == "View":
                    message = splitMessage(messages[f'scrim{sub_option}'], interaction.guild.id)
                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action} -> {pressed}", description=f"**Viewing {sub_option} Message**\n\n{message}", color=White)
                    await interaction.send(embed=embed, view=change_message_view(interaction, option, sub_option, action), ephemeral=True)

                elif pressed == "Edit":
                    message_raw = unformatMessage(messages[f'scrim{sub_option}'], interaction.guild.id)
                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action} -> {pressed}", description=f"**Editing {sub_option} Message, Copy the message and click \"Ready\"**\n\n{message_raw}", color=White)
                    await interaction.send(embed=embed, view=edit_message_view(interaction, option, sub_option, action), ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class edit_message_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option, sub_option, action):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        actions = ["Ready", "Back"]

        for item in actions:
            if item == "Ready": button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.success)
            else: button = nextcord.ui.Button(label=item, style=nextcord.ButtonStyle.grey)
            button.callback = self.create_callback(option, sub_option, action, item)
            self.add_item(button)

    def create_callback(self, option, sub_option, action, pressed):
        async def callback(interaction: nextcord.Interaction):
            config_data = getConfigData(interaction.guild.id)
            messages = getMessages(interaction.guild.id)
            channels = getChannels(interaction.guild.id)
            try:
                if pressed == "Back":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif pressed == "Ready":
                    await interaction.response.send_modal(modal=edit_message_modal(interaction, option, sub_option, action))

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class edit_message_modal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction, option, sub_option, action):
        super().__init__(title=f"Change {sub_option} Message", timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        self.input = nextcord.ui.TextInput(
            style=TextInputStyle.paragraph,
            label=f"Change {sub_option} Message",
            placeholder="Enter Message",
            min_length=0,
            max_length=2000)

        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        config_data = getConfigData(interaction.guild.id)
        messages = getMessages(interaction.guild.id)
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response == None:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n**ERROR** | Message Cannot Be Empty", color=White)
                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

            else:
                DB[str(interaction.guild.id)]["Config"].update_one({"messages": {"$exists": True}}, {"$set": {f"messages.scrim{self.sub_option}": response}})

                scrim_info = getScrimInfo(interaction.guild.id)
                channel = interaction.guild.get_channel(channels[f'scrim{self.sub_option}Channel'])

                if self.sub_option == "Announcement": # If announcement message is changed
                    if scrim_info["scrimEpoch"].isnumeric() == True: # A scrim has been scheduled before
                        scrim_epoch = int(scrim_info["scrimEpoch"])

                        if scrim_epoch < time.time():
                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Message Updated To <#response>, Announcement Message Not Sent (Scrim in progress/not scheduled)", color=White)
                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        else: # Scrim has not started yet
                            if channels[f'scrim{self.sub_option}Channel'] != None:
                                messages = getMessages(interaction.guild.id)
                                message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                message_split = message.split("\n")
                                title = message_split[0]
                                description = '\n'.join(message_split[1:])

                                embed = nextcord.Embed(title=title, description=description, color=White)
                                await channel.send(embed=embed)

                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Message Updated To <#response>, Announcement Message Moved", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # No Channel Set
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Message Updated, Announcement Channel Not Set!", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    else: # No scrims have ever been scheduled
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nAnnouncement Message Updated To <#response>, Announcement Message Not Sent (Scrim in progress/not scheduled)", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif self.sub_option == "Checkin": # If checkin message is changed
                    if config_data['toggleCheckin'] == True: # Checkins are enabled
                        if scrim_info["scrimEpoch"].isnumeric() == True:
                            scrim_epoch = int(scrim_info["scrimEpoch"])
                            if scrim_epoch > time.time():
                                scrim_datetime = datetime.datetime.fromtimestamp(scrim_epoch)
                                current_datetime = datetime.datetime.now()
                                time_until_start = scrim_datetime - current_datetime
                                hours_until_start = time_until_start.total_seconds() / 3600

                                if hours_until_start < config_data['toggleCheckinTime']: # If it is time to open checkins
                                    if channels[f'scrim{self.sub_option}Channel'] != None:
                                        messages = getMessages(interaction.guild.id)
                                        message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                        message_split = message.split("\n")
                                        title = message_split[0]
                                        description = '\n'.join(message_split[1:])

                                        embed = nextcord.Embed(title=title, description=description, color=White)
                                        await channel.send(embed=embed)

                                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Message Updated To <#response>, Checkin Message Moved", color=White)
                                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                    else: # No Channel Set
                                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Message Updated, Checkin Channel Not Set!", color=White)
                                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                else: # Not time to open checkins
                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Message Updated To <#response>, Checkin Message Not Sent (Checkins Not Open)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # Scrims have already started/ended
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Message Updated To <#response>, Checkin Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        else: # No scrims have ever been scheduled
                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Message Updated To <#response>, Checkin Message Not Sent (Scrim in progress/not scheduled)", color=White)
                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    else: # Checkins are disabled
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nCheckin Message Updated To <#response>, Checkin Message Not Sent (Checkins Disabled)", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif self.sub_option == "Rules": # If rules message is changed
                    if channels[f'scrim{self.sub_option}Channel'] != None:
                        messages = getMessages(interaction.guild.id)
                        message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                        message_split = message.split("\n")
                        title = message_split[0]
                        description = '\n'.join(message_split[1:])

                        embed = nextcord.Embed(title=title, description=description, color=White)
                        await channel.send(embed=embed)

                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRules Message Updated To <#response>, Rules Message Moved", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    else: # No Channel Set
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRules Message Updated, Rules Channel Not Set!", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif self.sub_option == "Format": # If format message is changed
                    if channels[f'scrim{self.sub_option}Channel'] != None:
                        messages = getMessages(interaction.guild.id)
                        message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                        message_split = message.split("\n")
                        title = message_split[0]
                        description = '\n'.join(message_split[1:])

                        embed = nextcord.Embed(title=title, description=description, color=White)
                        await channel.send(embed=embed)

                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nFormat Message Updated To <#response>, Format Message Moved", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    else: # No Channel Set
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nFormat Message Updated, Format Channel Not Set!", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif self.sub_option == "Poi": # If poi message is changed
                    if config_data['togglePoi'] == True: # Poi selection is enabled
                        if scrim_info["scrimEpoch"].isnumeric() == True:
                            scrim_epoch = int(scrim_info["scrimEpoch"])
                            if scrim_epoch > time.time():
                                scrim_datetime = datetime.datetime.fromtimestamp(scrim_epoch)
                                current_datetime = datetime.datetime.now()
                                time_until_start = scrim_datetime - current_datetime
                                hours_until_start = time_until_start.total_seconds() / 3600

                                if hours_until_start < config_data['togglePoiTime']: # If it is time to open poi selection
                                    if channels[f'scrim{self.sub_option}Channel'] != None:
                                        messages = getMessages(interaction.guild.id)
                                        message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                        message_split = message.split("\n")
                                        title = message_split[0]
                                        description = '\n'.join(message_split[1:])

                                        embed = nextcord.Embed(title=title, description=description, color=White)
                                        await channel.send(embed=embed)

                                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Message Updated To <#response>, Poi Message Moved", color=White)
                                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                    else: # No Channel Set
                                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Message Updated, Poi Channel Not Set!", color=White)
                                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                                else: # Not time to open poi selection
                                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Message Updated To <#response>, Poi Message Not Sent (Poi Selection Not Open)", color=White)
                                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # Scrims have already started/ended
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Message Updated To <#response>, Poi Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        else: # No scrims have ever been scheduled
                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Message Updated To <#response>, Poi Message Not Sent (Scrim in progress/not scheduled)", color=White)
                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    else: # Poi selection is disabled
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nPoi Message Updated To <#response>, Poi Message Not Sent (Poi Selection Disabled)", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                elif self.sub_option == "Registration": # If registration message is changed
                    if scrim_info["scrimEpoch"].isnumeric() == True: # A scrim has been scheduled before
                        scrim_epoch = int(scrim_info["scrimEpoch"])

                        if scrim_epoch > time.time(): # Scrim has already started/ended
                            if channels[f'scrim{self.sub_option}Channel'] != None:
                                messages = getMessages(interaction.guild.id)
                                message = splitMessage(messages[f'scrim{self.sub_option}'], interaction.guild.id)
                                message_split = message.split("\n")
                                title = message_split[0]
                                description = '\n'.join(message_split[1:])

                                embed = nextcord.Embed(title=title, description=description, color=White)
                                await channel.send(embed=embed)

                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Message Updated To <#response>, Registration Message Not Sent (Scrim in progress/not scheduled)", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                            else: # No Channel Set
                                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Message Updated, Registration Channel Not Set!", color=White)
                                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                        else:
                            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Message Updated To <#response>, Registration Message Not Sent (Scrim in progress/not scheduled)", color=White)
                            await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                    else: # No scrims have ever been scheduled
                        embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n\nRegistration Message Updated To <#response>, Registration Message Not Sent (Scrim in progress/not scheduled)", color=White)
                        await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action} -> Edit** Message Updated", color=Green)
                await interaction.send(embed=embed, ephemeral=True)
                formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                await channel.send(embed=embed)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

class change_role_modal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction, option, sub_option, action):
        super().__init__(title=f"Change {sub_option} Role", timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        self.input = nextcord.ui.TextInput(
            style=TextInputStyle.short,
            label=f"Change {sub_option} Role",
            placeholder="Enter Role ID",
            min_length=0,
            max_length=20)

        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        config_data = getConfigData(interaction.guild.id)
        messages = getMessages(interaction.guild.id)
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                role = interaction.guild.get_role(response)
                if role == None:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n**ERROR** | Role ID Must Be A Valid Role", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

                else:
                    DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {"config.casterRole": response}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action}** Set To <@&{response}>", color=Green)
                    await interaction.send(embed=embed, ephemeral=True)
                    formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started\n **ERROR** | Role ID Must Be A Numerical Value (e.g 123456789)", color=White)
                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(e, command, interaction, error_traceback)

class reset_view(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option

        button = nextcord.ui.Button(label="Yes", style=nextcord.ButtonStyle.success)
        button.callback = self.create_callback("Yes")
        self.add_item(button)

        button = nextcord.ui.Button(label="No", style=nextcord.ButtonStyle.danger)
        button.callback = self.create_callback("No")
        self.add_item(button)

    def create_callback(self, response):
        async def callback(interaction: nextcord.Interaction):
            channels = getChannels(interaction.guild.id)
            log_channel = channels["scrimLogChannel"]
            try:
                if response == "Yes":
                    message_data = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"]
                    config_data = DB.Scrimotron.GlobalData.find_one({"defaultConfig": {"$exists": True}})["defaultConfig"]
                    channel_data = DB.Scrimotron.GlobalData.find_one({"defaultChannels": {"$exists": True}})["defaultChannels"]

                    DB[str(interaction.guild.id)]["Config"].delete_one({"messages": {"$exists": "true"}})
                    DB[str(interaction.guild.id)]["Config"].delete_one({"config": {"$exists": "true"}})
                    DB[str(interaction.guild.id)]["Config"].delete_one({"channels": {"$exists": "true"}})

                    DB[str(interaction.guild.id)]["Config"].insert_one({"messages": message_data, "config": config_data, "channels": channel_data})

                    DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {"channels.scrimLogChannel": log_channel}})
                    formatOutput(output=f"Config Data Reset by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="**CONFIG DATA RESET**\nMost aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="**CONFIG DATA RESET**", color=White)

                    embed.set_footer(text=f"Config Data Reset by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(log_channel)
                    await channel.send(embed=embed)

                else:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="**CONFIG RESET CANCLED**\nMost aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                    await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

            except Exception as e:
                error_traceback = traceback.format_exc()
                await errorResponse(e, command, interaction, error_traceback)
        return callback

class Command_configure_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="configure", description="Configure Scrimotron **Staff Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def configure(self, interaction: nextcord.Interaction):
        global command
        command = interaction.application_command.name
        userID = interaction.user.id
        guildID = int(interaction.guild.id)
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal", guildID=guildID)

        try: await interaction.response.defer(ephemeral=True)
        except: pass

        channels = getChannels(guildID)

        if channels["scrimLogChannel"] == None: # If the log channel is not set
            embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Set**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"", color=Red)
            await interaction.send(embed=embed, view=set_log_view(interaction), ephemeral=True)

        else:
            channel = interaction.guild.get_channel(channels["scrimLogChannel"])

            if channel == None: # if the channel is deleted
                embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Found**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"", color=Red)
                await interaction.send(embed=embed, view=set_log_view(interaction), ephemeral=True)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised with this command\nPick a button below to get started", color=White)
                await interaction.send(embed=embed, view=main_view(interaction), ephemeral=True)

def setup(bot):
    bot.add_cog(Command_configure_Cog(bot))