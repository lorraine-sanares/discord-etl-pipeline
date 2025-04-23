"""
Discord Channel History Exporter

This script builds on the previous “Guild Channel Exporter” by:
  1. Loading the saved channel structure from `guild_channels_with_threads.json`.
  2. Prompting the user to choose one of the available text channels by ID.
  3. Connecting to Discord and fetching the full message history of that channel.
  4. Serializing all messages (id, author, content, timestamp) into a JSON file
     named `<channel_id>_history.json`.

Environment Variables Required:
  • DARCY_KEY — Your Discord bot token  
  • GUILD_ID  — The integer ID of the target Discord guild

Usage:
  $ python export_history.py
"""

import os
import json
import discord
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. Load environment variables from .env
# -----------------------------------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DARYL_KEY")               # Discord bot token
GUILD_ID = int(os.getenv("TEST_SERVER_ID"))        # Target server ID (converted to int)

# -----------------------------------------------------------------------------
# 2. Read previously saved channel list to display options to the user
# -----------------------------------------------------------------------------
with open("guild_channels_with_threads.json", "r", encoding="utf-8") as f:
    guild_data = json.load(f)

print("Available channels:")
# list all channels in categories
for cat in guild_data["categories"]:
    for ch in cat["channels"]:
        print(f"  {ch['id']}: {ch['name']}")
# list ungrouped channels
for ch in guild_data["ungrouped"]:
    print(f"  {ch['id']}: {ch['name']}")

# -----------------------------------------------------------------------------
# 3. Prompt user to select a channel by its ID
# -----------------------------------------------------------------------------
channel_id = int(input("Enter the ID of the channel whose history you want to export: "))

# -----------------------------------------------------------------------------
# 4. Set up Discord client with necessary intents
# -----------------------------------------------------------------------------
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True  # Required to read message content

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """
    Once connected, fetch the selected channel object and export its full history.
    """
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"❌ Guild with ID {GUILD_ID} not found.")
        await client.close()
        return

    channel = guild.get_channel(channel_id)
    if channel is None:
        print(f"❌ Channel with ID {channel_id} not found in guild.")
        await client.close()
        return

    print(f"🔍 Fetching history for #{channel.name} (ID: {channel.id})…")
    messages = []
    # -----------------------------------------------------------------------------
    # 5. Iterate through the entire history, oldest first
    # -----------------------------------------------------------------------------
    async for msg in channel.history(limit=None, oldest_first=True):
        messages.append({
            "id": msg.id,
            "author": msg.author.name,
            "content": msg.content,
            "created_at": msg.created_at.isoformat()
        })

    # -----------------------------------------------------------------------------
    # 6. Write the messages out to a JSON file
    # -----------------------------------------------------------------------------
    output_filename = f"{channel_id}_history.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"✅ Exported {len(messages)} messages to {output_filename}")
    await client.close()


# -----------------------------------------------------------------------------
# 7. Start the Discord client
# -----------------------------------------------------------------------------
client.run(TOKEN)
