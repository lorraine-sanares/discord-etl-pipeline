"""
Discord Chat History Exporter (Batch)

This script:
  1. Loads `json_files/guild_channels_with_threads.json`.
  2. Fetches full message history for each text channel.
  3. Serializes messages into `json_files/<channel_name>_history.json`.

Environment Variables Required:
  • DARCY_KEY      — Your Discord bot token  
  • TEST_SERVER_ID — The integer ID of the target Discord guild

Usage:
  $ uv run discord_chat_history_exporter.py
"""

import os
import json
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

    for channel_id, channel_name in channel_info:
        channel = guild.get_channel(channel_id)
        if not isinstance(channel, TextChannel):
            print(f"⚠️ Skipping non-text: {channel_name}")
            continue

        safe = channel_name.replace(" ", "_")
        print(f"🔄 Exporting {channel_name}...")
        msgs = []
        async for msg in channel.history(limit=None):
            msgs.append({
                "channel_id": channel_id,
                "id": msg.id,
                "author": msg.author.name,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            })

        out_path = os.path.join("json_files", f"{safe}_history.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(msgs, f, ensure_ascii=False, indent=2)
        print(f"✅ Wrote {out_path} ({len(msgs)} messages)")

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)