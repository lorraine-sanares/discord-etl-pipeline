"""
Discord Chat History Exporter (Batch)

This script:
  1. Loads `json_files/guild_channels_with_threads.json`.
  2. Fetches full message history for each text channel.
  3. Serializes all messages into a single `chat_history.csv` file.

Environment Variables Required:
  • DARCY_KEY      — Your Discord bot token  
  • TEST_SERVER_ID — The integer ID of the target Discord guild

Usage:
  $ uv run discord_chat_history_exporter.py
"""

import os
import json
import csv
import discord
import ssl
from dotenv import load_dotenv
from discord import TextChannel

# Ensure output directory exists
os.makedirs("json_files", exist_ok=True)

# Disable SSL verification globally
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
TOKEN = os.getenv("DARCY_KEY")
GUILD_ID = int(os.getenv("TEST_SERVER_ID"))

# Load channels data
with open(os.path.join("json_files", "guild_channels_with_threads.json"), "r", encoding="utf-8") as f:
    guild_data = json.load(f)

# Build list of (id, name)
channel_info = []
for category in guild_data.get("categories", []):
    for ch in category.get("channels", []):
        channel_info.append((int(ch["id"]), ch["name"]))
for ch in guild_data.get("ungrouped", []):
    channel_info.append((int(ch["id"]), ch["name"]))

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"❌ Guild ID {GUILD_ID} not found.")
        await client.close()
        return

    all_messages = []
    total_messages = 0
    
    for channel_id, channel_name in channel_info:
        try:
            channel = guild.get_channel(channel_id)
            if not isinstance(channel, TextChannel):
                print(f"⚠️ Skipping non-text: {channel_name}")
                continue

            print(f"🔄 Exporting {channel_name}...")
            channel_messages = []
            async for msg in channel.history(limit=None):
                channel_messages.append({
                    "channel_id": channel_id,
                    "channel_name": channel_name,
                    "message_id": msg.id,
                    "author": msg.author.name,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat()
                })
            
            all_messages.extend(channel_messages)
            total_messages += len(channel_messages)
            print(f"✅ Exported {len(channel_messages)} messages from {channel_name}")
            
        except Exception as e:
            print(f"❌ Error exporting {channel_name}: {str(e)}")
            continue

    # Write all messages to a single CSV file
    csv_path = "chat_history.csv"
    try:
        with open(csv_path, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["channel_id", "channel_name", "message_id", "author", "content", "timestamp"])
            writer.writeheader()
            writer.writerows(all_messages)
        
        print(f"✅ Wrote {csv_path} ({total_messages} messages total)")
    except Exception as e:
        print(f"❌ Error writing CSV file: {str(e)}")

    await client.close()

if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except Exception as e:
        print(f"❌ Error running client: {str(e)}")