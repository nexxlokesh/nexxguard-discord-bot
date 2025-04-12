import discord
from discord.ext import commands
from discord import app_commands
import json
from main import Seemu  # Import from your main file

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class PersonalMessageBot(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @app_commands.command(name="sendpersonalmsg", description="Send a personal message to all server members.")
    async def send_personal_msg(self, interaction: discord.Interaction, message: str, link: str):
        # Get the server-specific configuration
        server_id = str(interaction.guild.id)
        authorized_user_ids = set(map(int, config["servers"].get(server_id, {}).get("AUTHORIZED_USER_IDS", [])))  # Convert string IDs to integers

        # Check if the user is authorized
        if interaction.user.id not in authorized_user_ids:
            await interaction.response.send_message("You do not have permissions to use this command.", ephemeral=True)
            return

        # Defer the response
        await interaction.response.defer(thinking=True)

        # Iterate through all members and send DM
        for member in interaction.guild.members:
            if member.bot:
                continue  # Skip bots
            try:
                await member.send(f"{message}\n{link}")
            except discord.Forbidden:
                print(f"Could not send a DM to {member.display_name}. They might have DMs disabled.")
            except Exception as e:
                print(f"An error occurred while sending DM to {member.display_name}: {e}")

        await interaction.followup.send("Messages sent to all members!", ephemeral=True)

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(PersonalMessageBot(bot))
