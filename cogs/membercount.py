import discord
from discord.ext import commands
from main import Seemu
import json

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class MemberCountTracker(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.update_member_count(guild)  # Initial update for each guild

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.update_member_count(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.update_member_count(member.guild)

    async def update_member_count(self, guild: discord.Guild):
        server_id = str(guild.id)

        # Retrieve MEMBER_COUNT_CHANNEL_ID from config, default to 0 if not found
        member_count_channel_id = config["servers"].get(server_id, {}).get("MEMBER_COUNT_CHANNEL_ID", 0)
        if member_count_channel_id == 0:
            print(f"No MEMBER_COUNT_CHANNEL_ID found for guild: {guild.name}")
            return  # Exit if no channel ID is found

        total_members = guild.member_count
        channel = self.bot.get_channel(int(member_count_channel_id))  # Convert to int for the channel ID

        if channel:
            try:
                # Preserve the original channel name and update it with the member count.
                original_name = channel.name.split(':')[0]  # Get the part before the colon
                await channel.edit(name=f"{original_name}: {total_members}")
                print(f"Updated channel name to: {original_name}: {total_members} in guild: {guild.name}")
            except discord.Forbidden:
                print("Bot lacks permission to edit the channel name.")
            except discord.HTTPException as e:
                print(f"Failed to edit channel name: {e}")

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(MemberCountTracker(bot))
