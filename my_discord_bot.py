import discord
from discord.ext import commands, tasks
import os

# Set intents to allow tracking of member updates and activities
intents = discord.Intents.default()
intents.members = True  # Allows the bot to track member updates
intents.presences = True  # Allows the bot to track member statuses
intents.message_content = True  # Enables privileged message content intent

# Create a bot instance with the specified command prefix
bot = commands.Bot(command_prefix="a.", intents=intents)

# Replace with your actual server (guild) ID and bot token
GUILD_ID = 1314209004049793095  # Your server ID here
VANITY_ROLE_NAME = "Vanity"  # Role to be assigned
VANITY_STATUS_KEYWORD = ".gg/rcane"  # Keyword or phrase in status to trigger role

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    track_vanity_status.start()  # Start the background task to track vanity statuses

@tasks.loop(seconds=2)  # Every 2 seconds, adjust as needed
async def track_vanity_status():
    guild = bot.get_guild(GUILD_ID)
    if guild:
        for member in guild.members:
            # Ensure we don't make redundant changes
            has_vanity_role = discord.utils.get(member.roles, name=VANITY_ROLE_NAME)
            has_vanity_status = False

            # Check if the member has a custom status (any status type)
            if member.activities:
                for activity in member.activities:
                    # Check if the activity contains the vanity keyword
                    if isinstance(activity, discord.CustomActivity) or isinstance(activity, discord.Activity):
                        if VANITY_STATUS_KEYWORD.lower() in str(activity.name).lower():
                            has_vanity_status = True
                            break  # No need to check other activities if we've already found the vanity status

            if has_vanity_status and not has_vanity_role:
                # If the member has the vanity status but doesn't have the role, add it
                role = discord.utils.get(guild.roles, name=VANITY_ROLE_NAME)
                if role:
                    await member.add_roles(role)
                    print(f"Assigned '{VANITY_ROLE_NAME}' role to {member.name}")
            elif not has_vanity_status and has_vanity_role:
                # If the member doesn't have the vanity status but has the role, remove it
                role = discord.utils.get(guild.roles, name=VANITY_ROLE_NAME)
                if role:
                    await member.remove_roles(role)
                    print(f"Removed '{VANITY_ROLE_NAME}' role from {member.name}")

@bot.event
async def on_member_update(before, after):
    # If a member's status changes, check for vanity status
    has_vanity_role_before = discord.utils.get(before.roles, name=VANITY_ROLE_NAME)
    has_vanity_role_after = discord.utils.get(after.roles, name=VANITY_ROLE_NAME)
    
    has_vanity_status_before = False
    has_vanity_status_after = False

    # Check both before and after status for vanity keyword
    for activity in before.activities:
        if isinstance(activity, discord.CustomActivity) or isinstance(activity, discord.Activity):
            if VANITY_STATUS_KEYWORD.lower() in str(activity.name).lower():
                has_vanity_status_before = True
                break

    for activity in after.activities:
        if isinstance(activity, discord.CustomActivity) or isinstance(activity, discord.Activity):
            if VANITY_STATUS_KEYWORD.lower() in str(activity.name).lower():
                has_vanity_status_after = True
                break

    # If status has changed and role needs to be added or removed
    if has_vanity_status_after and not has_vanity_role_after:
        role = discord.utils.get(after.guild.roles, name=VANITY_ROLE_NAME)
        if role:
            await after.add_roles(role)
            print(f"Assigned '{VANITY_ROLE_NAME}' role to {after.name}")
    
    elif not has_vanity_status_after and has_vanity_role_after:
        role = discord.utils.get(after.guild.roles, name=VANITY_ROLE_NAME)
        if role:
            await after.remove_roles(role)
            print(f"Removed '{VANITY_ROLE_NAME}' role from {after.name}")

# Run the bot with your bot's token
bot.run("MTI2NDUyNzc4Mzk3MTc4Njg3Nw.GgPXBD.-geQ38Cteg20U14MxgCV6wKO6OptdIWjWJpVHI")  # Replace this with your actual bot token