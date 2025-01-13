import discord
import requests
from discord.ext import commands

# Initialize bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="a.", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Loaded commands: {list(bot.commands)}")  # Log loaded commands

def fetch_roblox_user(username):
    url = f"https://users.roblox.com/v1/users/search?keyword={username}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            user = data["data"][0]
            user_id = user["id"]
            avatar_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420&format=png"
            profile_url = f"https://www.roblox.com/users/{user_id}/profile"
            return {
                "id": user_id,
                "display_name": user["displayName"],
                "username": user["name"],
                "avatar_url": avatar_url,
                "profile_url": profile_url,
            }
    return None

@bot.command()
async def roblox(ctx, username: str):
    print(f"Command invoked: roblox {username}")  # Debugging log
    user_data = fetch_roblox_user(username)
    if user_data:
        embed = discord.Embed(
            title=f"{user_data['display_name']}'s Roblox Profile",
            url=user_data["profile_url"],
            description=f"Click the link above to view {user_data['display_name']}'s profile.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=user_data["avatar_url"])
        embed.add_field(name="Username", value=user_data["username"], inline=True)
        embed.add_field(name="User ID", value=user_data["id"], inline=True)
        embed.set_footer(text="Roblox Profile Tracker")

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"User '{username}' not found on Roblox.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found: {ctx.invoked_with}")
    else:
        raise error

# Run the bot
bot.run("MTI2NDUyNzc4Mzk3MTc4Njg3Nw.GgPXBD.-geQ38Cteg20U14MxgCV6wKO6OptdIWjWJpVHI")  # Replace with your bot token