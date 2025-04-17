import os
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DARCY_KEY")
GUILD_ID = 748845402727645185  # Your server’s ID

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

    out = {
        "guild_id": GUILD_ID,
        "guild_name": guild.name,
        "categories": [],
        "ungrouped": []
    }

    def serialize(ch):
        """
        Serialize a channel or thread object into a dict.
        - channels have `position`
        - threads have `parent_id` and `created_at`
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

    # 1) Gather and sort all category channels
    categories = [c for c in guild.channels if isinstance(c, discord.CategoryChannel)]
    categories.sort(key=lambda c: c.position)

    for cat in categories:
        cat_entry = {
            "id": cat.id,
            "name": cat.name,
            "position": cat.position,
            "channels": []
        }

        # 2) For each channel in this category, sorted by position
        childs = [ch for ch in guild.channels if ch.category_id == cat.id]
        childs.sort(key=lambda ch: ch.position)

        for ch in childs:
            channel_entry = serialize(ch)

            # 3) If it's a ForumChannel or TextChannel, collect its active threads,
            #    sort them by creation time, and serialize them too.
            if isinstance(ch, (discord.ForumChannel, discord.TextChannel)):
                threads = sorted(ch.threads, key=lambda t: t.created_at)
                channel_entry["threads"] = [serialize(t) for t in threads]

            cat_entry["channels"].append(channel_entry)

        out["categories"].append(cat_entry)

    # 4) Handle ungrouped (no category) top‑level channels
    ungrouped = [ch for ch in guild.channels if ch.category is None]
    ungrouped.sort(key=lambda ch: ch.position)

    for ch in ungrouped:
        entry = serialize(ch)
        if isinstance(ch, (discord.ForumChannel, discord.TextChannel)):
            threads = sorted(ch.threads, key=lambda t: t.created_at)
            entry["threads"] = [serialize(t) for t in threads]
        out["ungrouped"].append(entry)

    # 5) Write everything out to JSON
    with open("guild_channels_with_threads.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("✅ Wrote guild_channels_with_threads.json")
    await client.close()


client.run(TOKEN)
