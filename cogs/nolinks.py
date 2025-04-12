import discord
import re  # For matching URLs using regex
from discord.ext import commands
from main import Seemu  # Your main bot class
import json

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class LinkModerator(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    # Utility method to check if a message contains a link
    def contains_link(self, message: str) -> bool:
        url_pattern = r"(https?://[^\s]+)"  # Regex pattern for URLs
        return re.search(url_pattern, message) is not None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return  # Ignore messages from bots

        # Get the server-specific configuration
        server_id = str(message.guild.id)
        authorized_user_ids = set(map(int, config["servers"][server_id].get("AUTHORIZED_USER_IDS", [])))  # Convert string IDs to integers

        if self.contains_link(message.content):
            if message.author.id not in authorized_user_ids:  # Use authorized_user_ids here
                await message.delete()  # Delete the message with the link
                await message.channel.send(
                    f"{message.author.mention} You do not have permission to send links to this server ‼"
                )
                print(f"Link deleted and warned: {message.author}")

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(LinkModerator(bot))
