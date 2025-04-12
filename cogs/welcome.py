import json
import discord
from discord.ext import commands
from main import Seemu

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

class Welcome(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Get the server-specific configuration
        server_id = str(member.guild.id)

        welcome_channel_id = config["servers"].get(server_id, {}).get("WELCOME_CHANNEL_ID", 0)
        welcome_channel = self.bot.get_channel(int(welcome_channel_id))

        if welcome_channel:
            # Create the embed with the welcome message and important links
            embed = discord.Embed(
                title="Welcome!",
                description=(
                    f"Welcome {member.mention} to **{member.guild.name}**! 🎉\n\n"
                    "Please check the following channels:"
                ),
                color=0xffe5ec
            )
            embed.set_thumbnail(url=member.display_avatar.url)

            # Fetch rules and main chat channels from server-specific config
            rules_channel_id = config["servers"].get(server_id, {}).get("RULES_CHANNEL_ID", 0)
            rules_channel = member.guild.get_channel(int(rules_channel_id))

            main_chat_channel_id = config["servers"].get(server_id, {}).get("MAIN_CHAT_CHANNEL_ID", 0)
            main_chat_channel = member.guild.get_channel(int(main_chat_channel_id))

            # Add fields with links if channels are found
            if rules_channel:
                embed.add_field(
                    name="Rules",
                    value=f"[Read the Rules]({rules_channel.jump_url})",
                    inline=True
                )
            else:
                print("Rules channel not found or invalid ID.")

            if main_chat_channel:
                embed.add_field(
                    name="Main Chat",
                    value=f"[Join the Main Chat]({main_chat_channel.jump_url})",
                    inline=True
                )
            else:
                print("Main chat channel not found or invalid ID.")

            # Add the server's current member count
            member_count = member.guild.member_count
            embed.add_field(
                name="Total Members",
                value=f"We now have {member_count} members in the server!",
                inline=False
            )

            # Add the custom welcome image
            welcome_image_url = config["servers"].get(server_id, {}).get("WELCOME_IMAGE_URL", None)
            if welcome_image_url:
                embed.set_image(url=welcome_image_url)
            else:
                print("Welcome image URL not found or invalid.")

            # Send the embed to the welcome channel
            await welcome_channel.send(embed=embed)
        else:
            print("Welcome channel not found or invalid ID.")

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(Welcome(bot))
