import os
import json
import discord
from dotenv import load_dotenv

# Load your bot token from the .env file
load_dotenv()
TOKEN = os.getenv("DARCY_KEY")

# Path to the JSON file you exported earlier
DATA_FILE = "guild_channels_with_threads.json"

# Configure intents so we can read thread history
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # 1. Load the exported guild+thread structure
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Find the thread ID for "g/chat"
    target_thread_id = None
    for cat in data["categories"]:
        for ch in cat["channels"]:
            # look for the forum channel that contains our thread
            if ch["id"] == 1354789313333825576:
                for t in ch.get("threads", []):
                    if t["name"] == "g/chat":
                        target_thread_id = t["id"]
                        break
        if target_thread_id:
            break

    if target_thread_id is None:
        print("❌ Could not find the g/chat thread in the JSON data.")
        await client.close()
        return

    # 3. Fetch the Thread object and pull the last 100 messages
    thread = await client.fetch_channel(target_thread_id)
    last_messages = [msg async for msg in thread.history(limit=100)]

    # 4. Serialize the messages to a simple list of dicts
    output = []
    for msg in last_messages:
        output.append({
            "id": msg.id,
            "author": msg.author.name,
            "content": msg.content,
            "created_at": msg.created_at.isoformat()
        })

    # 5. Write them out to a new JSON file
    with open("g_chat_last100.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✅ Wrote the last 100 messages from g/chat to g_chat_last100.json")
    await client.close()


client.run(TOKEN)
