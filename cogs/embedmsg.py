import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import json
from main import Seemu

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class CustomEmbed(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @app_commands.command(name="sendembed", description="Send a customizable embed message.")
    async def send_embed(self, interaction: discord.Interaction, title: str, description: str, image_url: str = None, role_name: str = None):
        # Fetch server-specific configuration
        server_id = str(interaction.guild.id)
        server_config = config["servers"].get(server_id, {})
        authorized_user_ids = server_config.get("AUTHORIZED_USER_IDS", [])

        # Check if the user is authorized
        if str(interaction.user.id) not in authorized_user_ids:
            await interaction.response.send_message("You do not have permissions to use this command.", ephemeral=True)
            return

        # Get the current channel where the command was invoked
        current_channel = interaction.channel

        # Create the embed message
        embed = discord.Embed(
            title=title,
            description=description.replace("\\n", "\n"),
            color=0xffe5ec
        )

        # Set the author field with the author's name and logo
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url  # Using user's display avatar
        )

        # Add an image if provided
        if image_url:
            embed.set_image(url=image_url)

        # Add role mention if provided
        if role_name:
            if role_name.lower() == "everyone":
                # Mention everyone in the description
                embed.description += "\n@everyone"  # Append everyone mention to the embed description
            elif role_name.lower() == "here":
                # Mention here in the description
                embed.description += "\n@here"  # Append here mention to the embed description
            else:
                role = get(interaction.guild.roles, name=role_name)  # Fetch role by name
                if role:
                    # Mention the role in the description
                    embed.description += f"\n{role.mention}"  # Append role mention to the embed description
                else:
                    await interaction.response.send_message("Role not found.", ephemeral=True)
                    return

        # Send the embed to the current channel
        await current_channel.send(embed=embed)
        await interaction.response.send_message("Embed sent successfully!", ephemeral=True)

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(CustomEmbed(bot))
