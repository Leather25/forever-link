import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import aiohttp
import uuid

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise RuntimeError("DISCORD_TOKEN is not set")

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sync slash commands
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

SERVER_CONFIG = {
    1456445351430193326: {  # SERVER ID
        "allowed_channels": [
            1456445910815998127,
            1456446004890177636,
            1456446202735497258,
            1467693772816125994
        ],
        "archive_channel": 1467370545275211840
    },

    1461901906996629536: {  # SERVER ID
        "allowed_channels": [
            1461902392101572739,
        ],
        "archive_channel": 1467370586794754254
        },
        
    1415095232952799254: {  # SERVER ID
        "allowed_channels": [
            1415095614848630814,
        ],
        "archive_channel": 1467531704490266769
    },
}

# Slash command
@bot.tree.command(name="forever", description="Create a permanent link for an image or gif")
@app_commands.describe(file="Upload an image or gif")
async def forever(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer(thinking=True)

    # Download the file
    async with aiohttp.ClientSession() as session:
        async with session.get(file.url) as resp:
            if resp.status != 200:
                await interaction.followup.send("Failed to download file.")
                return
            data = await resp.read()

    # Re-upload to Discord (Discord CDN links are effectively permanent)
    temp_name = f"{uuid.uuid4()}_{file.filename}"
    discord_file = discord.File(fp=bytes(data), filename=temp_name)

    await interaction.followup.send(
        content="Here is your forever link:",
        file=discord_file
    )

bot.run(TOKEN)
