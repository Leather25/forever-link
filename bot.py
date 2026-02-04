import discord
from discord.ext import commands
import aiohttp
import os

TOKEN = "MTQ2NzM2Nzk4OTY1MjQ5MjMyOA.GPnwEx.vHDrPWGcAI0ivsvlBmW48jmnPfc9LRoD0l6TJw"

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

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    guild_id = message.guild.id

    if guild_id not in SERVER_CONFIG:
        return

    config = SERVER_CONFIG[guild_id]

    if message.channel.id not in config["allowed_channels"]:
        return

    if not message.attachments:
        return

    archive_channel = bot.get_channel(config["archive_channel"])
    if not archive_channel:
        return

    for attachment in message.attachments:
        if attachment.filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp")
        ):
            temp_file = f"temp_{attachment.filename}"

            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status == 200:
                        with open(temp_file, "wb") as f:
                            f.write(await resp.read())

            sent = await archive_channel.send(
                content=f"Archived from {message.author.mention}",
                file=discord.File(temp_file)
            )

            os.remove(temp_file)

            forever_link = sent.attachments[0].url
            await message.reply(f"🔗 **Forever Link:** {forever_link}")

    await bot.process_commands(message)

bot.run(TOKEN)

