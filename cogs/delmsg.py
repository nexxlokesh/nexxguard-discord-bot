import discord
from discord import app_commands
from discord.ext import commands
import json
from main import Seemu

# Load the data from data.json
with open("data.json") as f:
    data = json.load(f)

class CommandCog(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @app_commands.command(name="delete_messages", description="Delete a specified number of messages if authorized.")
    @app_commands.describe(limit="The number of messages to delete")
    async def delete_messages(self, interaction: discord.Interaction, limit: int = 10):
        """Delete a specified number of messages in the channel if authorized."""
        
        # Get server-specific data
        server_id = str(interaction.guild_id)
        server_data = data["servers"].get(server_id)

        if not server_data:
            await interaction.response.send_message("This server is not configured.", ephemeral=True)
            return

        # Check if user is authorized
        authorized_user_ids = server_data.get("AUTHORIZED_USER_IDS", [])
        if str(interaction.user.id) in authorized_user_ids:
            # Defer response to avoid timeout
            await interaction.response.defer(ephemeral=True)
            
            # Delete messages in the channel
            deleted = await interaction.channel.purge(limit=limit)
            
            # Send follow-up message after purging
            await interaction.followup.send(f"Deleted {len(deleted)} messages.")
        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

async def setup(bot: Seemu):
    await bot.add_cog(CommandCog(bot))
