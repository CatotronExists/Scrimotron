from discord import TextInputStyle
import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, errorResponse, getConfigData, getChannels, getMessages, DB, splitMessage, unformatMessage
from BotData.colors import *
from BotData.configurationdata import Data

class SetLogView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        button = nextcord.ui.Button(label="Set", style=nextcord.ButtonStyle.blurple)
        button.callback = self.create_callback()
        self.add_item(button)

    def create_callback(self):
        async def callback(interaction: nextcord.Interaction):
            try: await interaction.response.send_modal(modal=SetLogModal(interaction))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class SetLogModal(nextcord.ui.Modal):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__("Channel ID", timeout=None)
        self.interaction = interaction

        self.input = nextcord.ui.TextInput(
            label="Channel ID",
            placeholder="Enter Channel ID",
            min_length=0,
            max_length=20
        )

        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                channel = interaction.guild.get_channel(response)
                if channel != None:
                    DB[str(interaction.guild.id)]["Config"].update_one({"channels": {"$exists": True}}, {"$set": {f"channels.scrimLogChannel": response}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**Channels -> Log -> Change Channel** Set To <#{response}>", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)

                    formatOutput(output=f"Channels Log Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    await channel.send(embed=embed)

                else: # Channel Not Found
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Set**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"\n\n**ERROR** | Channel ID Must Be A Valid Channel", color=Red)
                    await interaction.response.edit_message(embed=embed, view=SetLogView(interaction), ephemeral=True)

            else: # Non numerical input
                embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Set**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"\n\n**ERROR** | Channel ID Must Be A Numerical Value (e.g 123456789)", color=Red)
                await interaction.response.edit_message(embed=embed, view=SetLogView(interaction), ephemeral=True)

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

class MainView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

        for option in Data.keys():
            button = nextcord.ui.Button(label=option, style=nextcord.ButtonStyle.blurple)
            button.callback = self.create_callback(option)
            self.add_item(button)

        button = nextcord.ui.Button(label="RESET", style=nextcord.ButtonStyle.danger)
        button.callback = self.create_callback("RESET")
        self.add_item(button)

    def create_callback(self, option): # Show Sub Options
        async def callback(interaction: nextcord.Interaction):
            try:
                config_data = getConfigData(interaction.guild.id)
                messages = getMessages(interaction.guild.id)
                channels = getChannels(interaction.guild.id)

                if option != "RESET": # Not Reset
                    embed = nextcord.Embed(title=f"{"Scrimotron Configuration"} -> {option}", description=f"Change {option} Options", color=White)
                    for sub_option in Data[option]:
                        if Data[option][sub_option]["Type"] == "Automation": value = f"{config_data[f'toggle{sub_option}']} | Set to {config_data[f'toggle{sub_option}Time']} hour(s) before start"

                        elif Data[option][sub_option]["Type"] == "Role":
                            if config_data['casterRole'] == None: value = f"{config_data['caster']} | Role: **Not Set**"
                            else: value = f"{config_data['caster']} | Role: <@&{config_data['casterRole']}>"

                        elif Data[option][sub_option]["Type"] == "Message":
                            default_message = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"][f"scrim{sub_option}"]
                            if messages[f'scrim{sub_option}'] == default_message: value = "**Default Message** | Click to View/Edit"
                            else: value = f"**Custom Message** | Click to View/Edit"

                        elif Data[option][sub_option]["Type"] == "Channel":
                            if channels[f"scrim{sub_option}Channel"] == None: value = "**Not Set**"
                            else: value = f"<#{channels[f'scrim{sub_option}Channel']}>"

                        embed.add_field(name=sub_option, value=value, inline=False)
                    await interaction.response.edit_message(embed=embed, view=SubView(interaction, option))

                else:
                    embed = nextcord.Embed(title="**RESET CONFIG DATA?**", description="Are you sure you want to reset all config data?\n*Only log channel settings will remain!*", color=Red)
                    await interaction.response.edit_message(embed=embed, view=ResetView(interaction, option))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class SubView(nextcord.ui.View):
    def __init__(self, interaction: nextcord.Interaction, option):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option

        for sub_option in Data[option]:
            button = nextcord.ui.Button(label=sub_option, style=nextcord.ButtonStyle.blurple)
            button.callback = self.create_callback(sub_option)
            self.add_item(button)

        button = nextcord.ui.Button(label="Back", style=nextcord.ButtonStyle.grey)
        button.callback = self.create_callback("Back")
        self.add_item(button)

    def create_callback(self, sub_option): # Show Sub Sub Options
        async def callback(interaction: nextcord.Interaction):
            try:
                if sub_option == "Back":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

                else:
                    config_data = getConfigData(interaction.guild.id)
                    messages = getMessages(interaction.guild.id)
                    channels = getChannels(interaction.guild.id)

                    embed = nextcord.Embed(title=f"{"Scrimotron Configuration"} -> {self.option} -> {sub_option}", description=f"Change {sub_option} Options", color=White)
                    if Data[self.option][sub_option]["Type"] == "Automation": value = f"{config_data[f'toggle{sub_option}']} | Set to {config_data[f'toggle{sub_option}Time']} hour(s) before start"

                    elif Data[self.option][sub_option]["Type"] == "Role":
                        if config_data['casterRole'] == None: value = f"{config_data['caster']} | Role: **Not Set**"
                        else: value = f"{config_data['caster']} | Role: <@&{config_data['casterRole']}>"

                    elif Data[self.option][sub_option]["Type"] == "Message":
                        default_message = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"][f"scrim{sub_option}"]
                        if messages[f'scrim{sub_option}'] == default_message: value = "**Default Message** | Click to View/Edit"
                        else: value = f"**Custom Message** | Click to View/Edit"

                    elif Data[self.option][sub_option]["Type"] == "Channel":
                        if channels[f"scrim{sub_option}Channel"] == None: value = "**Not Set**"
                        else: value = f"<#{channels[f'scrim{sub_option}Channel']}>"

                    embed.add_field(name=sub_option, value=value, inline=False)
                    await interaction.response.edit_message(embed=embed, view=SubSubView(interaction, self.option, sub_option))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class SubSubView(nextcord.ui.View): # Enable/Disable or change view
    def __init__(self, interaction: nextcord.Interaction, option, sub_option):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option

        config_data = getConfigData(interaction.guild.id)

        for button_label in Data[option][sub_option]["Options"]:
            current = None
            if button_label == "Enable":
                if sub_option == "Setup": current = config_data[f'toggle{sub_option}']
                elif sub_option == "Caster": current = config_data['caster']

                if current == True: # Enable button is disabled
                    button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.success, disabled=True)
                else: # Enable button is enabled
                    button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.success, disabled=False)

            elif button_label == "Disable":
                if sub_option == "Setup": current = config_data[f'toggle{sub_option}']
                elif sub_option == "Caster": current = config_data['caster']

                if current == False: # Disable button is disabled
                    button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.danger, disabled=True)
                else:  # Disable button is enabled
                    button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.danger, disabled=False)

            else: button = nextcord.ui.Button(label=button_label, style=nextcord.ButtonStyle.blurple)

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
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

                else:
                    if action == "Enable" or action == "Disable":
                        if action == "Enable": new_value = True
                        elif action == "Disable": new_value = False

                        if option == "Automation": DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {f"config.toggle{sub_option}": new_value}})
                        elif option == "Scrims": DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {"config.caster": new_value}})

                        embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option}** {action.lower()}d", color=Green)
                        await interaction.response.edit_message(embed=embed, view=None)
                        formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=command['guildID'])

                        embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                        channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                        await channel.send(embed=embed)

                    elif action == "Change Timing":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Timing", color=White)
                        embed.add_field(name=sub_option, value=f"Set to **{config_data[f"toggle{sub_option}Time"]}** hour(s) before start")
                        await interaction.response.send_modal(modal=ChangeTimingModal(interaction, option, sub_option, action))

                    elif action == "Change Channel":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Channel", color=White)
                        if channels[f"scrim{sub_option}Channel"] == None: embed.add_field(name=sub_option, value="**Not Set**")
                        else: embed.add_field(name=sub_option, value=f"Set to <#{channels[f'scrim{sub_option}Channel']}>")
                        await interaction.response.send_modal(modal=ChangeChannelModal(interaction, option, sub_option, action))

                    elif action == "Change Message":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Message", color=White)
                        default_message = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"][f"scrim{sub_option}"]
                        if messages[f'scrim{sub_option}'] == default_message: embed.add_field(name=sub_option, value="**Default Message** | Click to View/Edit")
                        else: embed.add_field(name=sub_option, value=f"**Custom Message** | Click to View/Edit")
                        await interaction.response.edit_message(embed=embed, view=ChangeMessageView(interaction, option, sub_option, action))

                    elif action == "Change Role":
                        embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action}", description=f"Change {sub_option} Role", color=White)
                        if config_data['casterRole'] == None: embed.add_field(name=sub_option, value="**Not Set**", inline=False)
                        else: embed.add_field(name=sub_option, value=f"Set to <@&{config_data['casterRole']}>", inline=False)
                        await interaction.response.send_modal(modal=ChangeRoleModal(interaction, option, sub_option, action))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class ChangeTimingModal(nextcord.ui.Modal):
    def __init__(self, interaction, option, sub_option, action):
        super().__init__("Timing", timeout=None)
        self.interaction = interaction
        self.option = option
        self.sub_option = sub_option
        self.action = action

        self.input = nextcord.ui.TextInput(
            label="Timing",
            placeholder="Enter hours before start (1-48)",
            min_length=0,
            max_length=20)

        self.input.callback = self.callback
        self.add_item(self.input)
    
    async def callback(self, interaction: nextcord.Interaction):
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                if response < 1 or response > 48:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Time Cannot Be Less Than One Hour or More Than 48 Hours", color=White)
                    await interaction.response.edit_message(embed=embed, view=None)

                else:
                    DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {f"config.toggle{self.sub_option}Time": response}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action}** Set to {response} hour(s) before start", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)
                    formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Time Must Be A Numerical Value (e.g 1, 2, 3)", color=White)
                await interaction.response.edit_message(embed=embed, view=MainView(interaction))

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

class ChangeChannelModal(nextcord.ui.Modal):
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
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                channel = interaction.guild.get_channel(response)
                if channel == None:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Channel ID Must Be A Valid Channel", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

                else:
                    DB[str(interaction.guild.id)]["Config"].update_one({"channels": {"$exists": True}}, {"$set": {f"channels.scrim{self.sub_option}Channel": response}})

                    if self.sub_option == "Log": note = "Logs will now be sent to the new channel"
                    elif self.sub_option == "Rules" or self.sub_option == "Format": # Move Rules and Format message
                        note = f"{self.sub_option} message has been been moved to the new channel"
                        message = splitMessage(getMessages(command['guildID'])[f"scrim{self.sub_option}"], interaction.guild.id, None)

                        embed = nextcord.Embed(title=message[0], description=message[1], color=White)
                        await channel.send(embed=embed)

                    else: note = "Future messages will be sent to the new channel"

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action}** Set To <#{response}>\n{note}", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)
                    formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    if self.sub_option == "Log": channel = interaction.guild.get_channel(response)
                    else: channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Channel ID Must Be A Numerical Value (e.g 123456789)", color=White)
                await interaction.response.edit_message(embed=embed, view=MainView(interaction))

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

class ChangeMessageView(nextcord.ui.View):
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
            messages = getMessages(interaction.guild.id)
            channels = getChannels(interaction.guild.id)

            try:
                if pressed == "Cancel":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

                elif pressed == "Reset":
                    default_message = DB.Scrimotron.GlobalData.find_one({"defaultMessages": {"$exists": True}})["defaultMessages"][f"scrim{sub_option}"]
                    DB[str(interaction.guild.id)]["Messages"].update_one({"messages": {"$exists": True}}, {"$set": {f"messages.scrim{sub_option}": default_message}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{option} -> {sub_option} -> {action}** Reset To Default Message", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)
                    formatOutput(output=f"{option} {sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{option} -> {sub_option} -> {action}** Reset To Default Message", color=Green)
                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

                elif pressed == "View":
                    message = splitMessage(messages[f'scrim{sub_option}'], interaction.guild.id)
                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action} -> {pressed}", description=f"**Viewing {sub_option} Message**\n\n{message}", color=White)
                    await interaction.response.edit_message(embed=embed, view=ChangeMessageView(interaction, option, sub_option, action))

                elif pressed == "Edit":
                    message_raw = unformatMessage(messages[f'scrim{sub_option}'])
                    embed = nextcord.Embed(title=f"Scrimotron Configuration -> {option} -> {sub_option} -> {action} -> {pressed}", description=f"**Editing {sub_option} Message, Copy the message and click \"Ready\"**\n\n{message_raw}", color=White)
                    await interaction.response.edit_message(embed=embed, view=EditMessageView(interaction, option, sub_option, action))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class EditMessageView(nextcord.ui.View):
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
            try:
                if pressed == "Back":
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

                elif pressed == "Ready":
                    await interaction.response.send_modal(modal=EditMessageModal(interaction, option, sub_option, action))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class EditMessageModal(nextcord.ui.Modal):
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
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response == None:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Message Cannot Be Empty", color=White)
                await interaction.response.edit_message(embed=embed, view=MainView(interaction))

            else:
                DB[str(interaction.guild.id)]["Config"].update_one({"messages": {"$exists": True}}, {"$set": {f"messages.scrim{self.sub_option}": response}})

                if self.sub_option == "Rules" or self.sub_option == "Format": 
                    channel = interaction.guild.get_channel(channels[f"scrim{self.sub_option}Channel"])

                    if channel == None:
                        note = f"{self.sub_option} has been updated, but could not be sent, no channel has been set"
                        embed = nextcord.Embed(title="Scrimotron Configuration", description=f"Most aspects of the bot can be customised\nPick a button below to get started\n\n**WARNING** | {self.sub_option} message could not be sent, no channel has been set\nSet the channel and the message will be sent!", color=Yellow)

                    else:
                        note = f"{self.sub_option} has been updated to the new message"
                        message = splitMessage(getMessages(command['guildID'])[f"scrim{self.sub_option}"], interaction.guild.id, None)
                        embed = nextcord.Embed(title=message[0], description=message[1], color=White)
                        await channel.send(embed=embed)
                
                else: note = f"Future {self.sub_option.lower()} messages will use the updated message"

                embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action}** Updated\n{note}", color=Green)
                await interaction.response.edit_message(embed=embed, view=None)
                formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                await channel.send(embed=embed)

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

class ChangeRoleModal(nextcord.ui.Modal):
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
            max_length=20
        )

        self.input.callback = self.callback
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        channels = getChannels(interaction.guild.id)

        response = self.input.value
        try:
            if response.isnumeric() == True:
                response = int(response)

                role = interaction.guild.get_role(response)
                if role == None:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Role ID Must Be A Valid Role", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

                else:
                    DB[str(interaction.guild.id)]["Config"].update_one({"config": {"$exists": True}}, {"$set": {"config.casterRole": response}})

                    embed = nextcord.Embed(title="Scrimotron Configuration", description=f"**{self.option} -> {self.sub_option} -> {self.action}** Set To <@&{response}>", color=Green)
                    await interaction.response.edit_message(embed=embed, view=None)
                    formatOutput(output=f"{self.option} {self.sub_option} Updated by {interaction.user.id} | @{interaction.user.name}", status="Normal", guildID=interaction.guild.id)

                    embed.set_footer(text=f"Config Updated by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(channels["scrimLogChannel"])
                    await channel.send(embed=embed)

            else:
                embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**ERROR** | Role ID Must Be A Numerical Value (e.g 123456789)", color=White)
                await interaction.response.edit_message(embed=embed, view=MainView(interaction))

        except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

class ResetView(nextcord.ui.View):
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
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**CONFIG DATA RESET**", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="**CONFIG DATA RESET**", color=White)

                    embed.set_footer(text=f"Config Data Reset by @{interaction.user.name}")
                    channel = interaction.guild.get_channel(log_channel)
                    await channel.send(embed=embed)

                else:
                    embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started\n\n**CONFIG RESET CANCLED**", color=White)
                    await interaction.response.edit_message(embed=embed, view=MainView(interaction))

            except Exception as e: await errorResponse(e, command, interaction, traceback.format_exc())

        return callback

class Command_configure_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="configure", description="Configure Scrimotron **Admin Only**", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def configure(self, interaction: nextcord.Interaction):
        global command
        command = {"name": interaction.application_command.name, "userID": interaction.user.id, "guildID": interaction.guild.id}
        formatOutput(output=f"/{command['name']} Used by {command['userID']} | @{interaction.user.name}", status="Normal", guildID=command["guildID"])

        try: await interaction.response.defer(ephemeral=True)
        except: pass # Discord can sometimes error on defer()

        channels = getChannels(command["guildID"])
        channel = interaction.guild.get_channel(channels["scrimLogChannel"])

        if channel == None: # If the log channel is not set/no longer exists
            embed = nextcord.Embed(title="Scrimotron Configuration", description="**Log Channel Not Set**\nA log channel is nessesary for the bot to function correctly\nThe log channel should be private and only viewable by mods/admins. Copy the Channel ID and click \"Set\"", color=Red)
            await interaction.edit_original_message(embed=embed, view=SetLogView(interaction))

        else: # Log channel exists and is set
            embed = nextcord.Embed(title="Scrimotron Configuration", description="Most aspects of the bot can be customised\nPick a button below to get started", color=White)
            await interaction.edit_original_message(embed=embed, view=MainView(interaction))

def setup(bot):
    bot.add_cog(Command_configure_Cog(bot))