import discord
from discord.ext import commands
import json
from main import Seemu  # Import from your main file

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class Auto(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Fetch server-specific configuration
        server_id = str(member.guild.id)
        server_config = config["servers"].get(server_id, {})
        
        # Get the member role name from the server configuration
        member_role_name = server_config.get("MEMBER_ROLE_NAME", "Members")  # Default to "Members" if not found
        role = discord.utils.get(member.guild.roles, name=member_role_name)
        
        if role:
            await member.add_roles(role)
            print(f'{member} ko "{member_role_name}" role diya gaya!')
        else:
            print(f'"{member_role_name}" role nahi mila!')

# Setup function to load the Cog.
async def setup(bot: Seemu):
    await bot.add_cog(Auto(bot))
