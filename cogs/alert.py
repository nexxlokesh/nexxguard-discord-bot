import discord
from discord.ext import commands
from discord import app_commands
import json
from main import Seemu  # Import from your main file

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class Alert(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @app_commands.command(name="alertmsg", description="Send a personal message to all members with the clients role.")
    async def send_personal_msg(self, interaction: discord.Interaction, message: str):
        # Fetch server-specific configuration
        server_id = str(interaction.guild.id)
        server_config = config["servers"].get(server_id, {})
        
        # Check if the user is authorized
        authorized_user_ids = server_config.get("AUTHORIZED_USER_IDS", [])
        if str(interaction.user.id) not in authorized_user_ids:
            await interaction.response.send_message("You do not have permissions to use this command.", ephemeral=True)
            return

        # Defer the response
        await interaction.response.defer(thinking=True)

        # Get the client role ID from server configuration
        client_role_id = server_config.get("CLIENT_ROLE_ID")
        client_role = discord.utils.get(interaction.guild.roles, id=client_role_id)
        if not client_role:
            await interaction.followup.send("Clients role not found.", ephemeral=True)
            return

        # Send an alert message as an embed to each member with the 'clients' role
        for member in interaction.guild.members:
            if member.bot or client_role not in member.roles:
                continue  # Skip bots and members without the clients role
            
            # Create an embed message
            embed = discord.Embed(
                title="Important Alert",
                description=f"🛑 {message}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Please read this message carefully.")
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

            try:
                # Send a DM with the embed to each eligible member
                await member.send(f"Hi {member.mention}, you have an important message:", embed=embed)
            except discord.Forbidden:
                print(f"Could not send a DM to {member.display_name}. They might have DMs disabled.")
            except Exception as e:
                print(f"An error occurred while sending DM to {member.display_name}: {e}")

        await interaction.followup.send("Messages sent to all members with the clients role!", ephemeral=True)

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(Alert(bot))
