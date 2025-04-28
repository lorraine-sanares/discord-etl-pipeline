"""
Discord Guild Channel Exporter

This script connects to a Discord guild (server) using credentials stored in a `.env` file,
retrieves the full hierarchy of categories and text channels, and serializes
that structure into JSON under `json_files/guild_channels_with_threads.json`.

Environment Variables Required:
  • DARCY_KEY      — Your Discord bot token  
  • TEST_SERVER_ID — The integer ID of the target Discord guild

Usage:
  $ uv run discord_guild_channel_exporter.py
"""

import os
import json
import discord
import ssl
from dotenv import load_dotenv

# Ensure output directory exists
os.makedirs("json_files", exist_ok=True)

# Disable SSL verification globally
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    load_dotenv()
    TOKEN = os.getenv("DARCY_KEY")
    GUILD_ID = int(os.getenv("TEST_SERVER_ID"))

    intents = discord.Intents.default()
    intents.guilds = True
    intents.guild_messages = True
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print(f"❌ Guild with ID {GUILD_ID} not found.")
            await client.close()
            return

        out = {"guild_id": guild.id, "guild_name": guild.name, "categories": [], "ungrouped": []}
        for category in guild.categories:
            cat = {"id": category.id, "name": category.name, "channels": []}
            for ch in category.text_channels:
                cat["channels"].append({"id": ch.id, "name": ch.name, "type": str(ch.type)})
            out["categories"].append(cat)
        for ch in guild.text_channels:
            if ch.category is None:
                out["ungrouped"].append({"id": ch.id, "name": ch.name, "type": str(ch.type)})

        path = os.path.join("json_files", "guild_channels_with_threads.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"✅ Wrote {path}")
        await client.close()

    client.run(TOKEN)


if __name__ == "__main__":
    main()