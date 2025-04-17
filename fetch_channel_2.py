import os
import json
import discord
from dotenv import load_dotenv

# 1. Load .env
load_dotenv()
TOKEN = os.getenv("DARCY_KEY")
GUILD_ID = 748845402727645185 # DS cubed server id

# 2. Set up intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"❌ Could not find guild ID {GUILD_ID}")
        await client.close()
        return

    # 3. Collect categories
    categories = [c for c in guild.channels if isinstance(c, discord.CategoryChannel)]
    categories.sort(key=lambda c: c.position)

    def children_of(cat):
        chs = [ch for ch in guild.channels if ch.category_id == cat.id]
        chs.sort(key=lambda ch: ch.position)
        return chs

    # 4. Build structure
    data = {"guild_id": GUILD_ID, "guild_name": guild.name, "categories": [], "ungrouped": []}

    for cat in categories:
        data["categories"].append({
            "id": cat.id,
            "name": cat.name,
            "position": cat.position,
            "channels": [
                {
                    "id": ch.id,
                    "name": ch.name,
                    "type": ch.type.name,
                    "position": ch.position
                }
                for ch in children_of(cat)
            ]
        })

    # 5. Ungrouped channels
    ungrouped = [ch for ch in guild.channels if ch.category is None]
    ungrouped.sort(key=lambda ch: ch.position)
    data["ungrouped"] = [
        {
            "id": ch.id,
            "name": ch.name,
            "type": ch.type.name,
            "position": ch.position
        }
        for ch in ungrouped
    ]

    # 6. Dump to JSON file
    with open("guild_channels.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Wrote channel structure for “{guild.name}” to guild_channels.json")
    await client.close()

client.run(TOKEN)
