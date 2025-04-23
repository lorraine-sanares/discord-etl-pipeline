"""
Discord Guild Channel Exporter

This script connects to a Discord guild (server) using credentials stored in a `.env` file,
retrieves the full hierarchy of categories, channels, and active threads, and serializes
that structure into a JSON file named `guild_channels_with_threads.json`.

Key Features:
  1. Loads `DARCY_KEY` (bot token) and `GUILD_ID` (server ID) from environment.
  2. Uses Discord.py with appropriate intents to access guild data.
  3. Collects all category channels, their child channels, and any threads.
  4. Gathers top‑level channels not assigned to a category.
  5. Outputs a neatly formatted JSON representation for easy archival or inspection.

Environment Variables Required:
  • DARCY_KEY — Your Discord bot token  
  • GUILD_ID  — The integer ID of the target Discord guild

Usage:
  $ python client.py

Output:
  A file `guild_channels_with_threads.json` with the following structure:
    {
      "guild_id": <int>,
      "guild_name": <str>,
      "categories": [ { ... } ],
      "ungrouped": [ { ... } ]
    }
"""

import os
import json
import discord
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. Load environment variables from the .env file
# -----------------------------------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DARYL_KEY")               # Discord bot token
GUILD_ID = int(os.getenv("TEST_SERVER_ID"))        # Target server ID (converted to int)

# -----------------------------------------------------------------------------
# 2. Configure Discord intents
#    We need access to guilds, messages, and message content
# -----------------------------------------------------------------------------
intents = discord.Intents.default()
intents.guilds = True                        # Enable guild (server) events
intents.guild_messages = True                # Enable guild message events
intents.message_content = True               # Enable reading message content

# -----------------------------------------------------------------------------
# 3. Instantiate the Discord client with our intents
# -----------------------------------------------------------------------------
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """
    Called once when the bot has connected and is ready.
    Fetches the specified guild and serializes its channels and threads to JSON.
    """
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        # If we can't find the guild, print an error and exit
        print(f"❌ Guild with ID {GUILD_ID} not found.")
        await client.close()
        return

    # Prepare the output structure
    out = {
        "guild_id": GUILD_ID,
        "guild_name": guild.name,
        "categories": [],   # will hold category groups and their channels
        "ungrouped": []     # will hold top-level channels not in any category
    }

    def serialize(ch):
        """
        Convert a channel or thread object into a serializable dict.
        - Always include id, name, and type.
        - Include position for channels.
        - Include parent_id and created_at for threads.
        """
        data = {
            "id": ch.id,
            "name": ch.name,
            "type": ch.type.name
        }
        if hasattr(ch, "position"):
            data["position"] = ch.position
        if hasattr(ch, "parent_id"):
            data["parent_id"] = ch.parent_id
        if hasattr(ch, "created_at"):
            data["created_at"] = ch.created_at.isoformat()
        return data

    # -----------------------------------------------------------------------------
    # 4. Gather all category channels, sorted by their position in the guild
    # -----------------------------------------------------------------------------
    categories = [c for c in guild.channels if isinstance(c, discord.CategoryChannel)]
    categories.sort(key=lambda c: c.position)

    for cat in categories:
        # Build the JSON entry for this category
        cat_entry = {
            "id": cat.id,
            "name": cat.name,
            "position": cat.position,
            "channels": []
        }

        # Find all channels belonging to this category, sorted by position
        children = [ch for ch in guild.channels if ch.category_id == cat.id]
        children.sort(key=lambda ch: ch.position)

        for ch in children:
            # Serialize each channel
            channel_entry = serialize(ch)

            # If the channel supports threads, include them
            if isinstance(ch, (discord.ForumChannel, discord.TextChannel)):
                threads = sorted(ch.threads, key=lambda t: t.created_at)
                channel_entry["threads"] = [serialize(t) for t in threads]

            cat_entry["channels"].append(channel_entry)

        out["categories"].append(cat_entry)

    # -----------------------------------------------------------------------------
    # 5. Handle ungrouped channels (those not in any category)
    # -----------------------------------------------------------------------------
    ungrouped = [ch for ch in guild.channels if ch.category is None]
    ungrouped.sort(key=lambda ch: ch.position)

    for ch in ungrouped:
        entry = serialize(ch)
        if isinstance(ch, (discord.ForumChannel, discord.TextChannel)):
            threads = sorted(ch.threads, key=lambda t: t.created_at)
            entry["threads"] = [serialize(t) for t in threads]
        out["ungrouped"].append(entry)

    # -----------------------------------------------------------------------------
    # 6. Write the serialized data to a JSON file
    # -----------------------------------------------------------------------------
    with open("guild_channels_with_threads.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("✅ Wrote guild_channels_with_threads.json")
    await client.close()


# -----------------------------------------------------------------------------
# 7. Start the bot
# -----------------------------------------------------------------------------
client.run(TOKEN)
