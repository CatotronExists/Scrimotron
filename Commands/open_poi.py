import nextcord
import datetime
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_poi
from Config import db_bot_data

class Command_open_poi_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[guildID], name="open_poi", description="Open POI selections", default_member_permissions=(nextcord.Permissions(administrator=True)))
    async def poi_open(self, interaction: nextcord.Interaction, 
        map1 = nextcord.SlashOption(name="map_1", description="Choose map 1", required=True, choices={"World's Edge": "Worlds Edge", "Olympus": "Olympus", "King's Canyon": "Kings Canyon", "Storm Point": "Storm Point", "Broken Moon": "Broken Moon"}),
        map2 = nextcord.SlashOption(name="map_2", description="Choose map 2", required=True, choices={"World's Edge": "Worlds Edge", "Olympus": "Olympus", "King's Canyon": "Kings Canyon", "Storm Point": "Storm Point", "Broken Moon": "Broken Moon"})
        ):
        command = 'open_poi'
        userID = interaction.user.id
        formatOutput(output="/"+command+" Used by ("+str(userID)+")", status="Normal")
        await interaction.send("Opening POI selections", ephemeral=True)

        try:
            try: db_bot_data.delete_one({"maps": {"$exists": True}}) # remove old maps
            except: pass
            embed = nextcord.Embed(title="POI Selections are Open!", description=f"Select a POI for {map1} & {map2} using /select_poi", color=0x000)
            embed.set_thumbnail(url="https://cdn.discordapp.com/icons/988302458533085234/6e2c8b045e0150185d14ffcd8cf6a2e3.png")
            await self.bot.get_channel(channel_poi).send(embed=embed)
            try: db_bot_data.update_one({"maps": {"map1": map1, "map2": map2}})
            except: 
                db_bot_data.insert_one({"maps": {
                "map1": map1,
                "map2": map2}
                })
            await interaction.edit_original_message(content=f"POI Selections opened for {map1} & {map2}")
            formatOutput(output=f"   POI Selections have been opened", status="Good")
            formatOutput(output=f"   /{command} was successful!", status="Good")

        except Exception as e:
            await errorResponse(error=e, command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_open_poi_Cog(bot))