import os
import discord
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DARCY_KEY")
GUILD_ID = 748845402727645185 # DS cubed server id

# Enable the intents we need
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot is online as {client.user}")
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"❌ Could not find a guild with ID {GUILD_ID}")
        await client.close()
        return

    # Gather all category channels and sort them by position
    categories = [c for c in guild.channels if isinstance(c, discord.CategoryChannel)]
    categories.sort(key=lambda c: c.position)

    def get_children(category):
        """Return all channels under a given category, sorted by position."""
        children = [ch for ch in guild.channels if ch.category_id == category.id]
        children.sort(key=lambda ch: ch.position)
        return children

    # Print each category and its child channels
    for cat in categories:
        print(f"📂 {cat.name}")
        for ch in get_children(cat):
            kind = (
                "💬 Text" if isinstance(ch, discord.TextChannel) else
                "🔊 Voice" if isinstance(ch, discord.VoiceChannel) else
                "📁 Thread" if isinstance(ch, discord.Thread) else
                "❓ Other"
            )
            print(f"   └─ {kind}  #{ch.name}")

    # Print channels that aren’t in any category
    ungrouped = [ch for ch in guild.channels if ch.category is None]
    ungrouped.sort(key=lambda ch: ch.position)
    if ungrouped:
        print("📂 Ungrouped Channels")
        for ch in ungrouped:
            kind = (
                "💬 Text" if isinstance(ch, discord.TextChannel) else
                "🔊 Voice" if isinstance(ch, discord.VoiceChannel) else
                "📁 Thread" if isinstance(ch, discord.Thread) else
                "❓ Other"
            )
            print(f"   └─ {kind}  #{ch.name}")

    # Gracefully close the bot
    await client.close()

client.run(TOKEN)
